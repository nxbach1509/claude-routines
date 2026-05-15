#!/usr/bin/env python3
"""Automated Vietnam Real Estate Market Report — daily mailer."""

from __future__ import annotations

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
MAX_TOKENS = 16000
MAX_TURNS = 20


def get_today_session() -> dict | None:
    """Return session config for today (Vietnam time), or None on Fri/Sat/Sun."""
    now = datetime.now(ICT)
    return SESSIONS.get(now.weekday())  # 0=Mon … 3=Thu; 4-6 → None


def generate_report(session: dict, date_str: str) -> str:
    """Call Claude with web-search tool and return the finished report text."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    prompt = build_prompt(session, date_str)

    log.info("Calling %s for Session %s …", MODEL, session["id"])

    messages: list[dict] = [{"role": "user", "content": prompt}]
    full_text_parts: list[str] = []

    # Tool-use loop: web_search_20250305 is server-side (Anthropic executes the
    # search); client passes back empty tool_result to acknowledge each turn.
    for turn in range(MAX_TURNS):
        for attempt in range(3):
            try:
                resp = client.messages.create(
                    model=MODEL,
                    max_tokens=MAX_TOKENS,
                    tools=[{"type": "web_search_20250305", "name": "web_search"}],
                    messages=messages,
                )
                break
            except anthropic.APIStatusError as exc:
                if attempt == 2:
                    raise
                wait = 2 ** attempt
                log.warning("API error (attempt %d): %s — retrying in %ds", attempt + 1, exc, wait)
                time.sleep(wait)

        tool_uses: list = []
        for block in resp.content:
            if hasattr(block, "text") and block.text:
                full_text_parts.append(block.text)
            elif getattr(block, "type", None) == "tool_use":
                tool_uses.append(block)

        log.info("Turn %d: stop_reason=%s, tool_uses=%d, text_chars=%d",
                 turn + 1, resp.stop_reason, len(tool_uses),
                 sum(len(p) for p in full_text_parts))

        if resp.stop_reason == "end_turn":
            break

        if resp.stop_reason == "tool_use" and tool_uses:
            # Append assistant turn and acknowledge server-side tool execution.
            messages.append({"role": "assistant", "content": resp.content})
            messages.append({
                "role": "user",
                "content": [
                    {"type": "tool_result", "tool_use_id": tu.id, "content": []}
                    for tu in tool_uses
                ],
            })
        else:
            log.warning("Unexpected stop_reason=%s — ending loop", resp.stop_reason)
            break
    else:
        log.warning("Reached MAX_TURNS=%d without end_turn", MAX_TURNS)

    full_text = "".join(full_text_parts)
    log.info("Report generated: %d chars", len(full_text))
    return full_text


def send_email(subject: str, body: str) -> None:
    sender = os.environ["GMAIL_SENDER"]
    password = os.environ["GMAIL_APP_PASSWORD"]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = RECIPIENT

    # Plain-text fallback
    msg.attach(MIMEText(body, "plain", "utf-8"))

    # HTML version — wraps body in a monospace block for alignment
    html_body = (
        "<html><body>"
        "<pre style='font-family:monospace;font-size:14px;line-height:1.5;"
        "white-space:pre-wrap;max-width:900px;'>"
        + body.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        + "</pre></body></html>"
    )
    msg.attach(MIMEText(html_body, "html", "utf-8"))

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
