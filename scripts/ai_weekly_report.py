#!/usr/bin/env python3
"""Automated AI Weekly Report — every Friday 07:30 ICT."""

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

from ai_weekly_prompt import build_ai_weekly_prompt

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


def _date_fmt(dt: datetime) -> str:
    return dt.strftime("%d/%m/%Y")


def get_report_meta() -> tuple[str, int, str, str]:
    """Return (date_str, iso_week_num, period_start, period_end) for today."""
    now = datetime.now(ICT)
    # Coverage: last Friday (7 days ago) → last Thursday (1 day ago)
    period_end_dt = now - timedelta(days=1)    # Thursday
    period_start_dt = now - timedelta(days=7)  # Previous Friday
    iso_week = now.isocalendar()[1]
    return (
        _date_fmt(now),
        iso_week,
        _date_fmt(period_start_dt),
        _date_fmt(period_end_dt),
    )


def generate_report(date_str: str, week_num: int, period_start: str, period_end: str) -> str:
    """Call Claude with web_search and return the finished report text."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    prompt = build_ai_weekly_prompt(date_str, week_num, period_start, period_end)

    log.info("Calling %s for AI Weekly Tuần %d …", MODEL, week_num)

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
    if now.weekday() != 4:  # 4 = Friday
        log.info("Not Friday (weekday=%d). Skipping.", now.weekday())
        return

    date_str, week_num, period_start, period_end = get_report_meta()
    log.info("AI Weekly Tuần %d | %s | Kỳ: %s – %s", week_num, date_str, period_start, period_end)

    body = generate_report(date_str, week_num, period_start, period_end)
    subject = f"AI Weekly — Tuần {week_num}, {date_str}"
    send_email(subject, body)
    log.info("Done ✓")


if __name__ == "__main__":
    main()
