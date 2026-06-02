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
# Use most capable model for McKinsey/BCG-grade research and analysis
MODEL = "claude-opus-4-8"
MAX_TOKENS = 16000
MAX_SEARCH_TURNS = 25


def get_today_session() -> dict | None:
    """Return session config for today (Vietnam time), or None on Fri/Sat/Sun.

    Set SESSION_OVERRIDE env var (A/B/C/D) to force a specific session (useful
    for manual workflow_dispatch testing).
    """
    override = os.environ.get("SESSION_OVERRIDE", "").strip().upper()
    if override:
        session = next((s for s in SESSIONS.values() if s["id"] == override), None)
        if session:
            log.info("SESSION_OVERRIDE=%s applied.", override)
            return session
        log.warning("SESSION_OVERRIDE=%s not recognized — ignoring.", override)

    now = datetime.now(ICT)
    return SESSIONS.get(now.weekday())  # 0=Mon … 3=Thu; 4-6 → None


def generate_report(session: dict, date_str: str) -> str:
    """Call Claude with web-search enabled and return the finished report text."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    prompt = build_prompt(session, date_str)

    log.info("Calling %s for Session %s …", MODEL, session["id"])

    messages: list[dict] = [{"role": "user", "content": prompt}]
    full_text = ""

    # Tool-use loop: web_search_20250305 is server-side (Anthropic executes the
    # search automatically). The client acknowledges each tool_use stop with
    # empty tool_result so Claude can continue generating the report.
    for _turn in range(MAX_SEARCH_TURNS):
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

        log.info(
            "Turn %d — stop_reason=%s, tool_uses=%d, text_chars=%d",
            _turn + 1,
            resp.stop_reason,
            len(tool_uses),
            len(full_text),
        )

        if resp.stop_reason == "end_turn":
            break

        if resp.stop_reason == "tool_use" and tool_uses:
            messages.append({"role": "assistant", "content": resp.content})
            # Acknowledge each tool use — the server has already executed the
            # search and stored results in its context; we send empty content.
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tu.id,
                        "content": "",
                    }
                    for tu in tool_uses
                ],
            })
        else:
            log.warning("Unexpected stop_reason=%s — exiting loop.", resp.stop_reason)
            break

    if not full_text.strip():
        raise RuntimeError("Report generation returned empty output — aborting email.")

    log.info("Report complete: %d chars, %d words.", len(full_text), len(full_text.split()))
    return full_text


def send_email(subject: str, body: str, max_retries: int = 4) -> None:
    """Send plain-text email via Gmail SMTP with exponential-backoff retry."""
    sender = os.environ["GMAIL_SENDER"]
    password = os.environ["GMAIL_APP_PASSWORD"]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = RECIPIENT
    msg.attach(MIMEText(body, "plain", "utf-8"))

    for attempt in range(1, max_retries + 1):
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(sender, password)
                smtp.sendmail(sender, [RECIPIENT], msg.as_string())
            log.info("Email sent → %s (subject: %s)", RECIPIENT, subject)
            return
        except smtplib.SMTPException as exc:
            if attempt == max_retries:
                raise
            wait = 2 ** attempt
            log.warning(
                "SMTP error attempt %d/%d: %s — retrying in %ds.",
                attempt, max_retries, exc, wait,
            )
            time.sleep(wait)


def main() -> None:
    session = get_today_session()
    if not session:
        log.info("No report today (Fri/Sat/Sun). Exiting.")
        return

    now = datetime.now(ICT)
    date_str = now.strftime("%d/%m/%Y")

    log.info(
        "=== Session %s: %s | %s, %s ===",
        session["id"],
        session["name"],
        session["thu"],
        date_str,
    )

    body = generate_report(session, date_str)
    subject = f"{session['email_prefix']} Deep Dive — {session['thu']}, {date_str}"
    send_email(subject, body)
    log.info("=== Done ✓ ===")


if __name__ == "__main__":
    main()
