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
MODEL = "claude-sonnet-4-6"
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

    # Tool-use loop: web_search_20250305 executes server-side.
    # On stop_reason="tool_use" we acknowledge with empty tool_result so the
    # model can continue; the actual search results are embedded in the next
    # assistant turn automatically.
    for _turn in range(20):
        resp = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            tools=[{"type": "web_search_20250305", "name": "web_search"}],
            messages=messages,
        )

        # Collect any text blocks emitted in this turn
        tool_uses: list = []
        for block in resp.content:
            if hasattr(block, "text"):
                full_text += block.text
            elif getattr(block, "type", None) == "tool_use":
                tool_uses.append(block)

        if resp.stop_reason == "end_turn":
            break

        # Acknowledge server-side tool calls so generation continues
        if resp.stop_reason == "tool_use" and tool_uses:
            messages.append({"role": "assistant", "content": resp.content})
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tu.id,
                        "content": "",  # server already has the result
                    }
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


def send_error_email(subject: str, error_msg: str) -> None:
    """Send a brief failure notification so the user knows the run broke."""
    try:
        body = (
            f"⚠️ Báo cáo tự động KHÔNG thể tạo hôm nay.\n\n"
            f"Lỗi: {error_msg}\n\n"
            f"Vui lòng kiểm tra:\n"
            f"  • ANTHROPIC_API_KEY còn credit: https://console.anthropic.com/settings/billing\n"
            f"  • GMAIL_SENDER và GMAIL_APP_PASSWORD hợp lệ\n"
            f"  • Log chi tiết: https://github.com/nxbach1509/claude-routines/actions\n"
        )
        send_email(subject, body)
        log.info("Error notification sent.")
    except Exception as mail_err:
        log.error("Could not send error notification: %s", mail_err)


def main() -> None:
    session = get_today_session()
    if not session:
        log.info("No report today (Fri/Sat/Sun).")
        return

    now = datetime.now(ICT)
    date_str = now.strftime("%d/%m/%Y")
    thu_str = session["thu"]
    subject = f"{session['email_prefix']} Deep Dive — {thu_str}, {date_str}"

    log.info("Session %s: %s — %s", session["id"], session["name"], date_str)

    try:
        body = generate_report(session, date_str)
    except anthropic.AuthenticationError as exc:
        log.error("Authentication failed — check ANTHROPIC_API_KEY: %s", exc)
        send_error_email(f"[LỖI] {subject}", str(exc))
        sys.exit(1)
    except anthropic.BadRequestError as exc:
        log.error("Anthropic API bad request (check credits / model name): %s", exc)
        send_error_email(f"[LỖI] {subject}", str(exc))
        sys.exit(1)
    except anthropic.APIStatusError as exc:
        log.error("Anthropic API error %s: %s", exc.status_code, exc)
        send_error_email(f"[LỖI] {subject}", str(exc))
        sys.exit(1)

    send_email(subject, body)
    log.info("Done ✓")


if __name__ == "__main__":
    main()
