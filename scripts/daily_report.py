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
MAX_SEARCH_USES = 15


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

    for _turn in range(20):
        resp = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            tools=[{
                "type": "web_search_20250305",
                "name": "web_search",
                "max_uses": MAX_SEARCH_USES,
            }],
            messages=messages,
        )

        if resp.stop_reason == "end_turn":
            full_text = "".join(
                block.text for block in resp.content if hasattr(block, "text")
            )
            log.info("Report generated: %d chars", len(full_text))
            return full_text

        if resp.stop_reason == "tool_use":
            tool_uses = [
                b for b in resp.content if getattr(b, "type", None) == "tool_use"
            ]
            if tool_uses:
                messages.append({"role": "assistant", "content": resp.content})
                messages.append({
                    "role": "user",
                    "content": [
                        {"type": "tool_result", "tool_use_id": tu.id, "content": []}
                        for tu in tool_uses
                    ],
                })
                continue

        # Unexpected stop or no tool uses — exit loop
        log.warning("Unexpected stop_reason=%s on turn %d", resp.stop_reason, _turn)
        full_text = "".join(
            block.text for block in resp.content if hasattr(block, "text")
        )
        log.info("Partial report collected: %d chars", len(full_text))
        return full_text

    log.warning("Reached max turns without end_turn")
    return ""


def send_email(subject: str, body: str, retries: int = 4) -> None:
    sender = os.environ["GMAIL_SENDER"]
    password = os.environ["GMAIL_APP_PASSWORD"]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = RECIPIENT
    msg.attach(MIMEText(body, "plain", "utf-8"))

    delay = 2
    for attempt in range(retries):
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(sender, password)
                smtp.sendmail(sender, [RECIPIENT], msg.as_string())
            log.info("Email sent → %s", RECIPIENT)
            return
        except Exception as exc:
            if attempt < retries - 1:
                log.warning(
                    "Send failed (attempt %d/%d): %s — retrying in %ds",
                    attempt + 1, retries, exc, delay,
                )
                time.sleep(delay)
                delay *= 2
            else:
                raise


def main() -> None:
    session = get_today_session()
    if not session:
        log.info("No report today (Fri/Sat/Sun).")
        return

    now = datetime.now(ICT)
    date_str = now.strftime("%d/%m/%Y")
    thu_str = session["thu"]

    log.info("Session %s: %s — %s", session["id"], session["name"], date_str)

    subject = f"{session['email_prefix']} Deep Dive — {thu_str}, {date_str}"

    try:
        body = generate_report(session, date_str)
        if not body.strip():
            body = "[LỖI] Báo cáo rỗng — vui lòng kiểm tra logs GitHub Actions."
    except Exception as exc:
        log.error("Report generation failed: %s", exc, exc_info=True)
        body = (
            f"[LỖI] Không thể tạo báo cáo hôm nay ({date_str}).\n\n"
            f"Chi tiết lỗi:\n{exc}\n\n"
            "Vui lòng kiểm tra logs GitHub Actions để biết thêm chi tiết."
        )

    send_email(subject, body)
    log.info("Done ✓")


if __name__ == "__main__":
    main()
