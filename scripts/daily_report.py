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
import markdown

from prompts import SESSIONS, build_prompt

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    stream=sys.stdout,
)
log = logging.getLogger(__name__)

ICT = ZoneInfo("Asia/Ho_Chi_Minh")
RECIPIENT = "nxbach1509@gmail.com"
MODEL = "claude-opus-4-7"   # Most capable; Sonnet is fine for cost-sensitive runs
MAX_TOKENS = 16_000
MAX_TOOL_TURNS = 25         # Cap multi-search loops


def get_today_session() -> dict | None:
    """Return session config for today (Vietnam time), or None on Fri/Sat/Sun."""
    now = datetime.now(ICT)
    return SESSIONS.get(now.weekday())  # 0=Mon … 3=Thu; 4-6 → None


def generate_report(session: dict, date_str: str) -> str:
    """Call Claude with web-search enabled and return the finished report text.

    web_search_20250305 is Anthropic's server-side hosted tool.  Claude emits
    tool_use blocks; the API executes the searches automatically.  We still
    need to drive the multi-turn loop: after each tool_use stop we re-submit
    the conversation with empty tool_result stubs so the model can continue
    incorporating the search data.
    """
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    prompt = build_prompt(session, date_str)

    log.info("Calling %s — Session %s …", MODEL, session["id"])

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
            if hasattr(block, "text") and block.text:
                full_text += block.text
            elif getattr(block, "type", None) == "tool_use":
                tool_uses.append(block)

        log.info("Turn %d — stop_reason=%s tools=%d text_len=%d",
                 turn, resp.stop_reason, len(tool_uses), len(full_text))

        if resp.stop_reason == "end_turn":
            break

        if resp.stop_reason == "tool_use" and tool_uses:
            # Acknowledge all tool calls; Anthropic injects actual results.
            messages.append({"role": "assistant", "content": resp.content})
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tu.id,
                        "content": [],
                    }
                    for tu in tool_uses
                ],
            })
        else:
            break   # Unexpected stop_reason — exit gracefully

    log.info("Report generated: %d chars", len(full_text))
    return full_text


def _plain_to_html(plain: str) -> str:
    """Convert the report (markdown + Unicode art) to a styled HTML email."""
    md_html = markdown.markdown(plain, extensions=["tables", "nl2br"])
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
  body  {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 14px;
           line-height: 1.65; color: #1a1a1a; background: #f5f5f5;
           margin: 0; padding: 20px; }}
  .card {{ background: #ffffff; border-radius: 8px; max-width: 820px;
           margin: 0 auto; padding: 32px 40px; box-shadow: 0 2px 8px rgba(0,0,0,.08); }}
  h1    {{ font-size: 20px; color: #0d47a1; border-bottom: 2px solid #e3f2fd;
           padding-bottom: 8px; }}
  h2    {{ font-size: 16px; color: #1565c0; margin-top: 28px; }}
  h3    {{ font-size: 14px; color: #1976d2; }}
  table {{ border-collapse: collapse; width: 100%; margin: 12px 0;
           font-size: 13px; }}
  th    {{ background: #e3f2fd; color: #0d47a1; padding: 6px 10px;
           text-align: left; border: 1px solid #bbdefb; }}
  td    {{ padding: 5px 10px; border: 1px solid #e0e0e0; }}
  tr:nth-child(even) td {{ background: #fafafa; }}
  ul,ol {{ margin: 8px 0; padding-left: 24px; }}
  li    {{ margin: 4px 0; }}
  code  {{ background: #f0f4ff; padding: 1px 4px; border-radius: 3px;
           font-size: 12px; }}
  pre   {{ background: #f0f4ff; padding: 12px; border-radius: 4px;
           overflow-x: auto; white-space: pre-wrap; font-size: 12px; }}
  .footer {{ margin-top: 32px; padding-top: 16px; border-top: 1px solid #e0e0e0;
             font-size: 12px; color: #757575; }}
</style>
</head>
<body>
<div class="card">
{md_html}
<div class="footer">Tổng hợp tự động bởi Claude · {datetime.now(ICT).strftime("%d/%m/%Y %H:%M")} ICT</div>
</div>
</body>
</html>"""


def _send_with_retry(sender: str, password: str, subject: str,
                     plain: str, html: str, max_retries: int = 4) -> None:
    """Send email over SMTP with exponential back-off on failure."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = RECIPIENT
    msg.attach(MIMEText(plain, "plain", "utf-8"))
    msg.attach(MIMEText(html, "html", "utf-8"))

    delay = 2
    last_err: Exception | None = None
    for attempt in range(1, max_retries + 1):
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(sender, password)
                smtp.sendmail(sender, [RECIPIENT], msg.as_string())
            log.info("Email sent → %s (attempt %d)", RECIPIENT, attempt)
            return
        except Exception as exc:
            last_err = exc
            log.warning("SMTP attempt %d failed: %s — retrying in %ds", attempt, exc, delay)
            time.sleep(delay)
            delay *= 2

    raise RuntimeError(f"Failed to send email after {max_retries} attempts") from last_err


def main() -> None:
    session = get_today_session()
    if not session:
        log.info("No report today (Fri/Sat/Sun — không gửi báo cáo).")
        return

    now = datetime.now(ICT)
    date_str = now.strftime("%d/%m/%Y")
    thu_str = session["thu"]

    log.info("Session %s: %s — %s", session["id"], session["name"], date_str)

    plain_body = generate_report(session, date_str)
    html_body = _plain_to_html(plain_body)
    subject = f"{session['email_prefix']} Deep Dive — {thu_str}, {date_str}"

    _send_with_retry(
        sender=os.environ["GMAIL_SENDER"],
        password=os.environ["GMAIL_APP_PASSWORD"],
        subject=subject,
        plain=plain_body,
        html=html_body,
    )
    log.info("Done ✓")


if __name__ == "__main__":
    main()
