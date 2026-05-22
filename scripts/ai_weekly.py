#!/usr/bin/env python3
"""Automated AI Weekly Report — Friday mailer."""

from __future__ import annotations

import logging
import os
import smtplib
import sys
from datetime import date, timedelta
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
MODEL = "claude-opus-4-7"
MAX_TOKENS = 16000


def get_report_period() -> tuple[int, str, str, str]:
    """Return (iso_week, date_str, start_date_str, end_date_str) in DD/MM/YYYY."""
    today = date.today()
    week_num = today.isocalendar()[1]

    # Period: last Friday → yesterday (Thursday)
    # today is Friday (weekday=4), so:
    #   last Friday = today - 7 days
    #   last Thursday = today - 1 day
    start = today - timedelta(days=7)
    end = today - timedelta(days=1)

    fmt = "%d/%m/%Y"
    return week_num, today.strftime(fmt), start.strftime(fmt), end.strftime(fmt)


def generate_report(
    date_str: str,
    start_date: str,
    end_date: str,
    week_num: int,
) -> str:
    """Call Claude with web-search and return the finished report text."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    prompt = build_ai_weekly_prompt(date_str, start_date, end_date, week_num)

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

    log.info("Email sent → %s | Subject: %s", RECIPIENT, subject)


def main() -> None:
    week_num, date_str, start_date, end_date = get_report_period()

    log.info(
        "AI Weekly Tuần %d | Kỳ: %s → %s | Ngày gửi: %s",
        week_num, start_date, end_date, date_str,
    )

    body = generate_report(date_str, start_date, end_date, week_num)

    # Subject: "AI Weekly — Tuần 21, 23/05/2025"
    subject = f"AI Weekly — Tuần {week_num}, {date_str}"
    send_email(subject, body)
    log.info("Done ✓")


if __name__ == "__main__":
    main()
