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
MODEL = "claude-opus-4-8"
MAX_TOKENS = 16000
MAX_SEARCH_TURNS = 25


def get_today_session() -> dict | None:
    """Return session config for today (Vietnam time), or None on Fri/Sat/Sun."""
    now = datetime.now(ICT)
    return SESSIONS.get(now.weekday())  # 0=Mon … 3=Thu; 4-6 → None


def _serialize_content(content: list) -> list[dict]:
    """Convert SDK content-block objects to plain dicts for message history."""
    result = []
    for block in content:
        if hasattr(block, "model_dump"):
            result.append(block.model_dump())
        elif isinstance(block, dict):
            result.append(block)
        else:
            result.append({"type": "text", "text": str(block)})
    return result


def generate_report(session: dict, date_str: str) -> str:
    """Call Claude with web-search enabled and return the finished report text."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    prompt = build_prompt(session, date_str)
    messages: list[dict] = [{"role": "user", "content": prompt}]

    log.info("Generating report for Session %s (%s)…", session["id"], session["name"])

    for turn in range(MAX_SEARCH_TURNS):
        resp = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            tools=[{"type": "web_search_20250305", "name": "web_search"}],
            messages=messages,
        )

        log.info("Turn %d: stop_reason=%s, blocks=%d", turn + 1, resp.stop_reason, len(resp.content))

        if resp.stop_reason == "end_turn":
            text = "".join(
                block.text for block in resp.content if hasattr(block, "text")
            )
            log.info("Report complete: %d chars", len(text))
            return text

        if resp.stop_reason == "tool_use":
            tool_uses = [b for b in resp.content if getattr(b, "type", None) == "tool_use"]
            if not tool_uses:
                # No tool_use blocks despite stop_reason — collect any text and exit
                break
            queries = [getattr(tu, "input", {}).get("query", "?") for tu in tool_uses]
            log.info("Searching: %s", queries)

            messages.append({"role": "assistant", "content": _serialize_content(resp.content)})
            messages.append({
                "role": "user",
                "content": [
                    {"type": "tool_result", "tool_use_id": tu.id, "content": []}
                    for tu in tool_uses
                ],
            })
            continue

        if resp.stop_reason == "max_tokens":
            log.warning("Max tokens hit on turn %d — collecting partial text", turn + 1)
            return "".join(b.text for b in resp.content if hasattr(b, "text"))

        log.warning("Unexpected stop_reason=%s on turn %d", resp.stop_reason, turn + 1)
        break

    raise RuntimeError(f"Report generation did not complete within {MAX_SEARCH_TURNS} turns")


def send_email(subject: str, body: str) -> None:
    sender = os.environ["GMAIL_SENDER"]
    password = os.environ["GMAIL_APP_PASSWORD"]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = RECIPIENT
    msg.attach(MIMEText(body, "plain", "utf-8"))

    last_exc: Exception | None = None
    for attempt in range(3):
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(sender, password)
                smtp.sendmail(sender, [RECIPIENT], msg.as_string())
            log.info("Email sent → %s (attempt %d)", RECIPIENT, attempt + 1)
            return
        except Exception as exc:
            last_exc = exc
            wait = 2 ** attempt
            log.warning("Send attempt %d failed: %s — retrying in %ds", attempt + 1, exc, wait)
            time.sleep(wait)

    raise RuntimeError(f"Failed to send email after 3 attempts: {last_exc}") from last_exc


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
