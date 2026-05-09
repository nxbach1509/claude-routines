#!/usr/bin/env python3
"""Automated Vietnam Real Estate Market Report — daily mailer."""

from __future__ import annotations

import argparse
import logging
import os
import smtplib
import sys
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from zoneinfo import ZoneInfo

import anthropic

from prompts import SESSIONS, build_prompt

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger(__name__)

ICT = ZoneInfo("Asia/Ho_Chi_Minh")
RECIPIENT = "nxbach1509@gmail.com"
MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 8192


def get_today_session(force_id: str | None = None) -> dict | None:
    """Return session config for today (Vietnam time), or None on Fri/Sat/Sun.

    Pass force_id='A'/'B'/'C'/'D' to override the day-of-week logic (for testing).
    """
    if force_id:
        for session in SESSIONS.values():
            if session["id"] == force_id.upper():
                return session
        raise ValueError(f"Unknown session id: {force_id!r}. Use A, B, C or D.")
    now = datetime.now(ICT)
    return SESSIONS.get(now.weekday())  # 0=Mon … 3=Thu; 4-6 → None


def generate_report(session: dict, date_str: str) -> str:
    """Call Claude (with server-side web search) and return the finished report."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    prompt = build_prompt(session, date_str)

    log.info("Calling %s for Session %s …", MODEL, session["id"])

    messages: list[dict] = [{"role": "user", "content": prompt}]
    full_text = ""

    # web_search_20250305 is a server-side tool: the API executes searches and
    # returns tool_use + tool_result blocks in the same response (stop_reason =
    # "end_turn"). The loop below is defensive — handles any future tool-use
    # round-trips gracefully.
    for _turn in range(20):
        resp = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            tools=[{"type": "web_search_20250305", "name": "web_search"}],
            messages=messages,
        )

        tool_uses: list = []
        for block in resp.content:
            if hasattr(block, "text"):
                full_text += block.text
            elif getattr(block, "type", None) == "tool_use":
                tool_uses.append(block)

        if resp.stop_reason == "end_turn":
            break

        if resp.stop_reason == "tool_use" and tool_uses:
            messages.append({"role": "assistant", "content": resp.content})
            messages.append({
                "role": "user",
                "content": [
                    {"type": "tool_result", "tool_use_id": tu.id, "content": ""}
                    for tu in tool_uses
                ],
            })
        else:
            break

    if not full_text.strip():
        raise RuntimeError("Report generation returned empty text — aborting.")

    log.info("Report generated: %d chars", len(full_text))
    return full_text


def _build_html(body: str) -> str:
    """Wrap the plain-text report in a minimal HTML shell for Gmail rendering."""
    # Escape HTML special chars only in the body content
    escaped = body.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f"""\
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {{
      background: #f4f4f4;
      margin: 0;
      padding: 20px;
      font-family: -apple-system, 'Segoe UI', Arial, sans-serif;
    }}
    .card {{
      max-width: 820px;
      margin: 0 auto;
      background: #ffffff;
      border-radius: 8px;
      padding: 32px 36px;
      box-shadow: 0 2px 8px rgba(0,0,0,.08);
    }}
    pre {{
      font-family: 'Courier New', 'Consolas', monospace;
      font-size: 13px;
      line-height: 1.65;
      white-space: pre-wrap;
      word-break: break-word;
      color: #1a1a1a;
      margin: 0;
    }}
    .footer {{
      margin-top: 24px;
      font-size: 11px;
      color: #888;
      text-align: center;
    }}
  </style>
</head>
<body>
  <div class="card">
    <pre>{escaped}</pre>
    <p class="footer">Tổng hợp tự động bởi Claude · {MODEL} · {datetime.now(ICT).strftime("%d/%m/%Y %H:%M")} ICT</p>
  </div>
</body>
</html>"""


def send_email(subject: str, body: str, dry_run: bool = False) -> None:
    if dry_run:
        log.info("[DRY-RUN] Subject: %s", subject)
        log.info("[DRY-RUN] Body preview (first 500 chars):\n%s", body[:500])
        return

    sender = os.environ["GMAIL_SENDER"]
    password = os.environ["GMAIL_APP_PASSWORD"]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = RECIPIENT
    msg.attach(MIMEText(body, "plain", "utf-8"))
    msg.attach(MIMEText(_build_html(body), "html", "utf-8"))

    # Retry up to 3 times with exponential backoff for transient SMTP errors
    for attempt in range(1, 4):
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(sender, password)
                smtp.sendmail(sender, [RECIPIENT], msg.as_string())
            log.info("Email sent → %s", RECIPIENT)
            return
        except smtplib.SMTPException as exc:
            if attempt == 3:
                raise
            wait = 2 ** attempt
            log.warning("SMTP attempt %d failed (%s) — retrying in %ds", attempt, exc, wait)
            time.sleep(wait)


def main() -> None:
    parser = argparse.ArgumentParser(description="Vietnam RE daily report mailer")
    parser.add_argument("--dry-run", action="store_true",
                        help="Generate report but print instead of sending email")
    parser.add_argument("--session", metavar="ID",
                        help="Force a specific session (A/B/C/D) regardless of day")
    args = parser.parse_args()

    session = get_today_session(force_id=args.session)
    if not session:
        log.info("No report today (Fri/Sat/Sun). Use --session A/B/C/D to force.")
        return

    now = datetime.now(ICT)
    date_str = now.strftime("%d/%m/%Y")
    thu_str = session["thu"]

    log.info("Session %s: %s — %s", session["id"], session["name"], date_str)

    body = generate_report(session, date_str)
    subject = f"{session['email_prefix']} Deep Dive — {thu_str}, {date_str}"
    send_email(subject, body, dry_run=args.dry_run)
    log.info("Done ✓")


if __name__ == "__main__":
    main()
