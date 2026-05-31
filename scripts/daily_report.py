#!/usr/bin/env python3
"""Automated Vietnam Real Estate Market Report — daily mailer."""

from __future__ import annotations

import logging
import os
import smtplib
import sys
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
MAX_TOKENS = 32_000
# Server-side web-search loops at most 10 iterations before pause_turn;
# allow up to 5 continuations so the model can do ~50 searches if needed.
MAX_CONTINUATIONS = 5

_TOOLS = [
    {"type": "web_search_20260209", "name": "web_search"},
    {"type": "web_fetch_20260209", "name": "web_fetch"},
]


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

    for _turn in range(MAX_CONTINUATIONS):
        resp = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            tools=_TOOLS,
            messages=messages,
        )

        for block in resp.content:
            if getattr(block, "type", None) == "text":
                full_text += block.text

        log.info(
            "Turn %d/%d: stop_reason=%s, cumulative_chars=%d",
            _turn + 1,
            MAX_CONTINUATIONS,
            resp.stop_reason,
            len(full_text),
        )

        if resp.stop_reason == "end_turn":
            break
        elif resp.stop_reason == "pause_turn":
            # Server-side tool loop hit its 10-iteration cap.
            # Append the assistant turn — the API detects the trailing
            # server_tool_use block and resumes automatically (no user message needed).
            messages.append({"role": "assistant", "content": resp.content})
        else:
            log.warning("Unexpected stop_reason=%s; halting.", resp.stop_reason)
            break

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
