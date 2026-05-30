#!/usr/bin/env python3
"""Automated Vietnam Real Estate Market Report — daily mailer."""

from __future__ import annotations

import argparse
import html
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
MODEL = "claude-opus-4-8"
MAX_TOKENS = 16000
BETAS = ["web-search-2025-03-05"]


# ---------------------------------------------------------------------------
# Day selection
# ---------------------------------------------------------------------------

def get_today_session(day_override: int | None = None) -> dict | None:
    """Return session config for today (Vietnam time), or None on Fri/Sat/Sun."""
    if day_override is not None:
        return SESSIONS.get(day_override)
    now = datetime.now(ICT)
    return SESSIONS.get(now.weekday())  # 0=Mon … 3=Thu; 4-6 → None


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(session: dict, date_str: str) -> str:
    """Call Claude with server-side web search and return the finished report."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    prompt = build_prompt(session, date_str)

    log.info("Model: %s | Session: %s | Date: %s", MODEL, session["id"], date_str)

    messages: list[dict] = [{"role": "user", "content": prompt}]
    full_text = ""

    for turn in range(25):
        # Use beta endpoint so the web_search_20250305 tool is recognised
        resp = client.beta.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            tools=[{"type": "web_search_20250305", "name": "web_search"}],
            messages=messages,
            betas=BETAS,
        )
        log.info("Turn %d — stop_reason: %s", turn + 1, resp.stop_reason)

        tool_uses: list = []
        for block in resp.content:
            if hasattr(block, "text"):
                full_text += block.text
            elif getattr(block, "type", None) == "tool_use":
                tool_uses.append(block)

        if resp.stop_reason == "end_turn":
            break

        if resp.stop_reason == "tool_use" and tool_uses:
            # Append assistant turn, then acknowledge each tool call.
            # For web_search_20250305, Anthropic executes the search server-side;
            # the client just needs to complete the loop with a tool_result.
            messages.append({"role": "assistant", "content": resp.content})
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tu.id,
                        "content": "",   # server fills actual results
                    }
                    for tu in tool_uses
                ],
            })
        else:
            break

    log.info("Report generated: %d chars", len(full_text))
    return full_text


# ---------------------------------------------------------------------------
# Email helpers
# ---------------------------------------------------------------------------

_HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  body {{
    margin: 0; padding: 0;
    background: #f0f2f5;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 14px;
    color: #1a1a2e;
  }}
  .wrapper {{
    max-width: 800px;
    margin: 24px auto;
    background: #ffffff;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,0.10);
  }}
  .header {{
    background: linear-gradient(135deg, #0d1b2a 0%, #1e3a5f 100%);
    color: #ffffff;
    padding: 28px 32px 22px;
  }}
  .header h1 {{
    margin: 0 0 6px;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 0.5px;
  }}
  .header p {{
    margin: 0;
    font-size: 12px;
    color: #93c5fd;
    font-style: italic;
  }}
  .body {{
    padding: 28px 32px;
  }}
  pre {{
    white-space: pre-wrap;
    word-break: break-word;
    font-family: 'Courier New', Courier, monospace;
    font-size: 13px;
    line-height: 1.7;
    color: #1a1a2e;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 20px 22px;
    margin: 0;
  }}
  .footer {{
    background: #f8fafc;
    border-top: 1px solid #e2e8f0;
    padding: 14px 32px;
    font-size: 11px;
    color: #94a3b8;
    text-align: center;
  }}
</style>
</head>
<body>
  <div class="wrapper">
    <div class="header">
      <h1>{title}</h1>
      <p>Tổng hợp tự động bởi Claude AI · {timestamp} (Giờ Việt Nam)</p>
    </div>
    <div class="body">
      <pre>{body}</pre>
    </div>
    <div class="footer">
      Báo cáo này được tạo tự động · Nguồn: Savills · CBRE · JLL · Và các nguồn công bố trong 7 ngày qua
    </div>
  </div>
</body>
</html>
"""


def _make_html(subject: str, body_text: str) -> str:
    now_str = datetime.now(ICT).strftime("%d/%m/%Y %H:%M")
    return _HTML_TEMPLATE.format(
        title=html.escape(subject),
        timestamp=now_str,
        body=html.escape(body_text),
    )


def send_email(subject: str, body: str) -> None:
    sender = os.environ["GMAIL_SENDER"]
    password = os.environ["GMAIL_APP_PASSWORD"]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = RECIPIENT

    msg.attach(MIMEText(body, "plain", "utf-8"))
    msg.attach(MIMEText(_make_html(subject, body), "html", "utf-8"))

    # Retry up to 3 times with exponential back-off
    for attempt in range(1, 4):
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(sender, password)
                smtp.sendmail(sender, [RECIPIENT], msg.as_string())
            log.info("Email sent → %s", RECIPIENT)
            return
        except Exception as exc:  # noqa: BLE001
            if attempt == 3:
                raise
            wait = 2 ** attempt
            log.warning("SMTP attempt %d failed (%s); retrying in %ds…", attempt, exc, wait)
            time.sleep(wait)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Vietnam RE daily report mailer")
    parser.add_argument(
        "--day",
        type=int,
        choices=[0, 1, 2, 3],
        default=None,
        help="Override weekday: 0=Mon 1=Tue 2=Wed 3=Thu (default: today Vietnam time)",
    )
    args = parser.parse_args()

    session = get_today_session(args.day)
    if not session:
        log.info("No report today (Fri/Sat/Sun).")
        return

    now = datetime.now(ICT)
    date_str = now.strftime("%d/%m/%Y")
    thu_str = session["thu"]

    log.info("Session %s: %s — %s", session["id"], session["name"], date_str)

    body = generate_report(session, date_str)
    subject = f"{session['email_prefix']} Deep Dive — {thu_str}, {date_str}"
    send_email(subject, body)
    log.info("Done ✓")


if __name__ == "__main__":
    main()
