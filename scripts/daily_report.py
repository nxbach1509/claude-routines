#!/usr/bin/env python3
"""Automated Vietnam Real Estate Market Report — daily mailer."""

from __future__ import annotations

import logging
import os
import smtplib
import sys
import textwrap
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


def get_today_session() -> dict | None:
    """Return session config for today (Vietnam time), or None on Fri/Sat/Sun."""
    now = datetime.now(ICT)
    return SESSIONS.get(now.weekday())  # 0=Mon … 3=Thu; 4-6 → None


def generate_report(session: dict, date_str: str) -> str:
    """Call Claude with web-search enabled and return the finished report text."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    prompt = build_prompt(session, date_str)

    log.info("Calling %s for Session %s …", MODEL, session["id"])

    messages: list[dict] = [{"role": "user", "content": prompt}]
    full_text = ""

    # Tool-use loop: handle web_search intermediate turns.
    # web_search_20250305 is Anthropic-hosted; results come back in the next turn.
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
                    {"type": "tool_result", "tool_use_id": tu.id, "content": []}
                    for tu in tool_uses
                ],
            })
        else:
            break

    log.info("Report generated: %d chars", len(full_text))
    return full_text


def _build_html(body: str) -> str:
    """Wrap the plain-text report in minimal HTML for nicer email rendering."""
    escaped = (
        body
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    return textwrap.dedent(f"""\
        <!DOCTYPE html>
        <html lang="vi">
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body style="margin:0;padding:16px;background:#f5f5f5;font-family:sans-serif;">
          <div style="max-width:800px;margin:0 auto;background:#ffffff;
                      border-radius:8px;padding:24px 28px;
                      border:1px solid #e0e0e0;">
            <pre style="font-family:'Courier New',Courier,monospace;
                        font-size:13px;line-height:1.6;
                        white-space:pre-wrap;word-break:break-word;
                        color:#222222;margin:0;">{escaped}</pre>
          </div>
          <p style="text-align:center;font-size:11px;color:#999;margin-top:12px;">
            Báo cáo tự động · Claude AI · Mọi số liệu cần được xác minh độc lập trước khi ra quyết định.
          </p>
        </body>
        </html>
    """)


def send_email(subject: str, body: str) -> None:
    sender = os.environ["GMAIL_SENDER"]
    password = os.environ["GMAIL_APP_PASSWORD"]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = RECIPIENT

    # Plain-text fallback first, HTML preferred part last (RFC 2046)
    msg.attach(MIMEText(body, "plain", "utf-8"))
    msg.attach(MIMEText(_build_html(body), "html", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, [RECIPIENT], msg.as_string())

    log.info("Email sent → %s", RECIPIENT)


def main() -> None:
    session = get_today_session()
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
