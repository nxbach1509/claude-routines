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
MODEL = "claude-opus-4-7"
MAX_TOKENS = 32000
MAX_TOOL_TURNS = 30


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

    for turn in range(MAX_TOOL_TURNS):
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

        log.info("Turn %d — stop_reason=%s tool_uses=%d text_so_far=%d chars",
                 turn + 1, resp.stop_reason, len(tool_uses), len(full_text))

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
            log.warning("Unexpected stop_reason=%s — breaking loop", resp.stop_reason)
            break

    if not full_text.strip():
        raise RuntimeError("Report generation returned empty text — aborting send.")

    log.info("Report generated: %d chars", len(full_text))
    return full_text


def send_email(subject: str, body: str) -> None:
    sender = os.environ["GMAIL_SENDER"]
    password = os.environ["GMAIL_APP_PASSWORD"]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = RECIPIENT
    msg.attach(MIMEText(body, "plain", "utf-8"))

    for attempt in range(3):
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(sender, password)
                smtp.sendmail(sender, [RECIPIENT], msg.as_string())
            log.info("Email sent → %s", RECIPIENT)
            return
        except Exception as exc:
            wait = 2 ** attempt
            log.warning("SMTP attempt %d failed: %s — retrying in %ds", attempt + 1, exc, wait)
            time.sleep(wait)

    raise RuntimeError("All SMTP attempts failed.")


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
