#!/usr/bin/env python3
"""Automated AI Weekly Report — Friday mailer."""

from __future__ import annotations

import logging
import os
import smtplib
import sys
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from zoneinfo import ZoneInfo

import anthropic

from ai_weekly_prompt import build_prompt

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


def _date_info(now: datetime) -> dict:
    """Return all date/week metadata needed for the report."""
    iso = now.isocalendar()
    week_num = iso[1]
    year = iso[0]
    date_str = now.strftime("%d/%m/%Y")
    # Coverage window: last 7 days (Fri–Thu)
    end_dt = now - timedelta(days=1)          # yesterday (Thu)
    start_dt = end_dt - timedelta(days=6)     # previous Fri
    start_date = start_dt.strftime("%d/%m/%Y")
    end_date = end_dt.strftime("%d/%m/%Y")
    # Generic month/year ref for search queries — Claude also uses the explicit date range above
    week_ref = end_dt.strftime("%B %Y")
    return {
        "date_str": date_str,
        "week_num": week_num,
        "year": year,
        "start_date": start_date,
        "end_date": end_date,
        "week_ref": week_ref,
    }


def generate_report(info: dict) -> str:
    """Call Claude with web-search enabled and return the finished report text."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    prompt = build_prompt(**info)

    log.info("Calling %s for AI Weekly Tuần %s …", MODEL, info["week_num"])

    messages: list[dict] = [{"role": "user", "content": prompt}]
    full_text = ""

    for _turn in range(30):
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
    now = datetime.now(ICT)
    info = _date_info(now)

    log.info(
        "AI Weekly — Tuần %s, %s (phạm vi: %s – %s)",
        info["week_num"], info["date_str"], info["start_date"], info["end_date"],
    )

    body = generate_report(info)
    subject = f"AI Weekly — Tuần {info['week_num']}, {info['date_str']}"
    send_email(subject, body)
    log.info("Done ✓")


if __name__ == "__main__":
    main()
