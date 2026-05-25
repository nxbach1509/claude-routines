#!/usr/bin/env python3
"""Automated Vietnam Real Estate Market Report — daily mailer."""

from __future__ import annotations

import logging
import os
import smtplib
import sys
import time
import traceback
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
MODEL = "claude-opus-4-7"   # Opus for highest analytical quality
MAX_TOKENS = 16000
_SMTP_HOST = "smtp.gmail.com"
_SMTP_PORT = 465


# ---------------------------------------------------------------------------
# Day detection
# ---------------------------------------------------------------------------

def get_today_session() -> dict | None:
    """Return session config for today (Vietnam time), or None on Fri/Sat/Sun."""
    now = datetime.now(ICT)
    return SESSIONS.get(now.weekday())  # 0=Mon … 3=Thu; 4-6 → None


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(session: dict, date_str: str) -> str:
    """Call Claude with web-search enabled and return the finished report text."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    prompt = build_prompt(session, date_str)

    log.info("Calling %s — Session %s …", MODEL, session["id"])

    messages: list[dict] = [{"role": "user", "content": prompt}]
    full_text = ""

    # Tool-use loop: web_search_20250305 is server-side on Anthropic's end.
    # stop_reason will be "end_turn" once searches + generation complete.
    # We loop up to 20 turns as a safety net for any intermediate stops.
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

        # If the model yields a tool_use stop (shouldn't happen for server-side
        # web_search, but handle defensively to avoid infinite hang).
        if resp.stop_reason == "tool_use" and tool_uses:
            messages.append({"role": "assistant", "content": resp.content})
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tu.id,
                        "content": "",   # empty: server already handled search
                    }
                    for tu in tool_uses
                ],
            })
        else:
            break

    log.info("Report generated: %d chars", len(full_text))
    return full_text


def _retry_generate(session: dict, date_str: str, max_attempts: int = 3) -> str:
    """Retry generate_report with exponential backoff on transient failures."""
    for attempt in range(1, max_attempts + 1):
        try:
            return generate_report(session, date_str)
        except (anthropic.APIConnectionError, anthropic.APITimeoutError) as exc:
            if attempt == max_attempts:
                raise
            wait = 2 ** attempt
            log.warning("API error on attempt %d/%d: %s — retrying in %ds …",
                        attempt, max_attempts, exc, wait)
            time.sleep(wait)
    raise RuntimeError("unreachable")


# ---------------------------------------------------------------------------
# Email sending
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
    color: #1a1a1a;
  }}
  .wrapper {{
    max-width: 800px;
    margin: 24px auto;
    background: #ffffff;
    border-radius: 10px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.10);
    overflow: hidden;
  }}
  .banner {{
    background: linear-gradient(135deg, #0d1b2a 0%, #1b3a5c 100%);
    color: #e8ecf0;
    padding: 22px 28px;
    letter-spacing: 0.02em;
  }}
  .banner h1 {{
    margin: 0 0 4px 0;
    font-size: 18px;
    font-weight: 700;
    color: #ffffff;
  }}
  .banner p {{
    margin: 0;
    font-size: 12px;
    color: #94a3b8;
  }}
  .body {{
    padding: 28px;
  }}
  pre {{
    white-space: pre-wrap;
    word-break: break-word;
    font-family: 'Courier New', 'Lucida Console', monospace;
    font-size: 13px;
    line-height: 1.75;
    color: #1e293b;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 20px;
    margin: 0;
  }}
  .footer {{
    border-top: 1px solid #e2e8f0;
    padding: 14px 28px;
    font-size: 11px;
    color: #94a3b8;
    text-align: center;
  }}
</style>
</head>
<body>
<div class="wrapper">
  <div class="banner">
    <h1>{subject}</h1>
    <p>Tổng hợp bởi Claude · {model} · {timestamp}</p>
  </div>
  <div class="body">
    <pre>{body_escaped}</pre>
  </div>
  <div class="footer">
    Báo cáo được tạo tự động mỗi ngày lúc 07:30 ICT (Thứ 2–5) · Không trả lời email này
  </div>
</div>
</body>
</html>
"""


def _escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
    )


def send_email(subject: str, body: str) -> None:
    sender = os.environ["GMAIL_SENDER"]
    password = os.environ["GMAIL_APP_PASSWORD"]

    now_str = datetime.now(ICT).strftime("%d/%m/%Y %H:%M ICT")
    html_body = _HTML_TEMPLATE.format(
        subject=_escape_html(subject),
        model=MODEL,
        timestamp=now_str,
        body_escaped=_escape_html(body),
    )

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"Vietnam RE Report <{sender}>"
    msg["To"] = RECIPIENT
    msg.attach(MIMEText(body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    for attempt in range(1, 4):
        try:
            with smtplib.SMTP_SSL(_SMTP_HOST, _SMTP_PORT, timeout=30) as smtp:
                smtp.login(sender, password)
                smtp.sendmail(sender, [RECIPIENT], msg.as_string())
            log.info("Email sent → %s", RECIPIENT)
            return
        except (smtplib.SMTPException, OSError) as exc:
            if attempt == 3:
                raise
            wait = 2 ** attempt
            log.warning("SMTP error attempt %d/3: %s — retrying in %ds …",
                        attempt, exc, wait)
            time.sleep(wait)


def send_error_email(error_msg: str, session_name: str, date_str: str) -> None:
    """Send a minimal notification if report generation fails."""
    try:
        sender = os.environ["GMAIL_SENDER"]
        password = os.environ["GMAIL_APP_PASSWORD"]
        subject = f"[ERROR] RE Report Failed — {session_name} {date_str}"
        body = (
            f"Báo cáo {session_name} ngày {date_str} THẤT BẠI.\n\n"
            f"Lỗi:\n{error_msg}\n\n"
            "Vui lòng kiểm tra GitHub Actions logs."
        )
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = RECIPIENT
        msg.attach(MIMEText(body, "plain", "utf-8"))
        with smtplib.SMTP_SSL(_SMTP_HOST, _SMTP_PORT, timeout=20) as smtp:
            smtp.login(sender, password)
            smtp.sendmail(sender, [RECIPIENT], msg.as_string())
        log.info("Error notification sent.")
    except Exception:
        log.exception("Could not send error notification.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    session = get_today_session()
    if not session:
        log.info("No report today (Fri/Sat/Sun). Exiting.")
        return

    now = datetime.now(ICT)
    date_str = now.strftime("%d/%m/%Y")
    thu_str = session["thu"]

    log.info("Starting Session %s: %s — %s", session["id"], session["name"], date_str)

    try:
        body = _retry_generate(session, date_str)
    except Exception:
        err = traceback.format_exc()
        log.error("Report generation failed:\n%s", err)
        send_error_email(err, session["name"], date_str)
        sys.exit(1)

    subject = f"{session['email_prefix']} Deep Dive — {thu_str}, {date_str}"
    send_email(subject, body)
    log.info("Done ✓")


if __name__ == "__main__":
    main()
