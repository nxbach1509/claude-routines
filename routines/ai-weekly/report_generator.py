#!/usr/bin/env python3
"""
AI Weekly Report Generator
Chạy tự động mỗi thứ Sáu 7:30 AM.
Tổng hợp tin AI 7 ngày qua → gửi email nxbach1509@gmail.com.
"""

import os
import sys
import json
import logging
import smtplib
import time
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from typing import Optional

try:
    import anthropic
except ImportError:
    print("ERROR: anthropic package not installed. Run: pip install -r requirements.txt")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*args, **kwargs):
        pass

# ── Logging ──────────────────────────────────────────────────────────────────

LOG_DIR = Path(__file__).parent.parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / f"ai_weekly_{datetime.now().strftime('%Y%m%d')}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# ── Date helpers ──────────────────────────────────────────────────────────────

def get_week_info() -> dict:
    today = datetime.now()
    iso = today.isocalendar()
    last_friday = today - timedelta(days=7)
    this_thursday = today - timedelta(days=1)
    return {
        "week_num": iso[1],
        "year": iso[0],
        "friday_date": today.strftime("%d/%m/%Y"),
        "last_friday": last_friday.strftime("%d/%m/%Y"),
        "this_thursday": this_thursday.strftime("%d/%m/%Y"),
        "date_range": f"{last_friday.strftime('%d/%m/%Y')} → {this_thursday.strftime('%d/%m/%Y')}",
        "search_month": today.strftime("%B %Y"),
    }

# ── Web search ────────────────────────────────────────────────────────────────

def search_tavily(query: str, api_key: str) -> str:
    import urllib.request
    payload = json.dumps({
        "api_key": api_key,
        "query": query,
        "search_depth": "advanced",
        "max_results": 6,
        "include_answer": True,
        "include_raw_content": False,
    }).encode()
    req = urllib.request.Request(
        "https://api.tavily.com/search",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
        parts = []
        if data.get("answer"):
            parts.append(f"[Summary] {data['answer']}")
        for r in data.get("results", []):
            snippet = (r.get("content") or "")[:300]
            parts.append(f"• {r['title']} ({r['url']}): {snippet}")
        return "\n".join(parts) or "No results."
    except Exception as exc:
        logger.warning(f"Tavily error for '{query}': {exc}")
        return f"Search failed: {exc}"


def search_duckduckgo(query: str) -> str:
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=6))
        parts = [f"• {r['title']} ({r['href']}): {r['body'][:250]}" for r in results]
        return "\n".join(parts) or "No results."
    except Exception as exc:
        logger.warning(f"DuckDuckGo error for '{query}': {exc}")
        return f"Search failed: {exc}"


def web_search(query: str, tavily_key: Optional[str]) -> str:
    logger.info(f"  🔍 {query}")
    if tavily_key:
        return search_tavily(query, tavily_key)
    return search_duckduckgo(query)

# ── Report generation via Anthropic SDK with tool use ─────────────────────────

SEARCH_QUERIES = [
    # Layer 1 — Hardware
    "NVIDIA Blackwell Rubin GPU AI chips news {month}",
    "AMD MI350 Intel Gaudi chip AI semiconductor news {month}",
    "AI data center power consumption nuclear energy infrastructure {month}",
    "Microsoft AWS Google Meta hyperscaler data center capex investment {month}",
    "SpaceX Starlink satellite internet AI news {month}",
    # Layer 2 — Data & Cloud
    "Microsoft Azure OpenAI AWS Bedrock Google Vertex AI new features {month}",
    "Databricks Snowflake vector database RAG AI tools {month}",
    "Apple Intelligence Qualcomm NPU on-device AI {month}",
    # Layer 3 — Models
    "Anthropic Claude new model features {month}",
    "OpenAI GPT o-series model release benchmark {month}",
    "Google Gemini DeepMind AI model update {month}",
    "Meta Llama open source model release {month}",
    "AI research paper arxiv breakthrough multimodal reasoning {month}",
    "xAI Grok Mistral DeepSeek Qwen AI model news {month}",
    # Layer 4 — Applications
    "AI real estate proptech AVM automated valuation {month}",
    "AI banking fintech algorithmic trading fraud detection {month}",
    "AI healthcare medical imaging drug discovery FDA approval {month}",
    "AI education edtech tutoring personalized learning {month}",
    "AI logistics airport autonomous drone supply chain {month}",
    "GitHub Copilot Cursor Salesforce Agentforce enterprise AI {month}",
]


def generate_report(week_info: dict, anthropic_key: str, tavily_key: Optional[str]) -> str:
    client = anthropic.Anthropic(api_key=anthropic_key)

    # Load prompt template
    tpl_path = Path(__file__).parent / "prompt_template.md"
    prompt = tpl_path.read_text(encoding="utf-8")
    for k, v in week_info.items():
        prompt = prompt.replace(f"[{k.upper()}]", str(v))

    # Define web_search tool for Claude
    tools = [
        {
            "name": "web_search",
            "description": (
                "Search the internet for recent AI news, research papers, and industry developments. "
                "Use targeted queries to find up-to-date information from the past 7 days."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Specific search query for AI news and developments",
                    }
                },
                "required": ["query"],
            },
        }
    ]

    messages = [{"role": "user", "content": prompt}]
    final_text = ""
    iteration = 0
    max_iterations = 40  # allow many search rounds

    logger.info("Starting Claude report generation with tool use loop...")

    while iteration < max_iterations:
        iteration += 1
        logger.info(f"Claude turn {iteration}")

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=16000,
            tools=tools,
            messages=messages,
        )

        # Collect text content
        text_blocks = [b.text for b in response.content if hasattr(b, "text")]
        tool_uses = [b for b in response.content if b.type == "tool_use"]

        if text_blocks:
            final_text = "\n".join(text_blocks)

        # Done when no tool calls remain
        if response.stop_reason == "end_turn" or not tool_uses:
            logger.info(f"Report complete after {iteration} turns.")
            break

        # Execute tool calls
        tool_results = []
        for tu in tool_uses:
            query = tu.input.get("query", "")
            result = web_search(query, tavily_key)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tu.id,
                "content": result,
            })

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})

    if not final_text:
        raise RuntimeError("Claude returned an empty report after all iterations.")

    return final_text

# ── Email sending ─────────────────────────────────────────────────────────────

def send_email(
    to_email: str,
    subject: str,
    body: str,
    gmail_user: str,
    gmail_password: str,
) -> None:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"AI Weekly <{gmail_user}>"
    msg["To"] = to_email

    # Plain text
    msg.attach(MIMEText(body, "plain", "utf-8"))

    # Simple HTML version (wrap plain text in <pre> for readability)
    html_body = (
        "<html><body>"
        '<div style="font-family:monospace;font-size:14px;line-height:1.6;'
        'max-width:800px;margin:auto;white-space:pre-wrap;">'
        f"{body}"
        "</div></body></html>"
    )
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    logger.info(f"Connecting to Gmail SMTP...")
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to_email, msg.as_string())

    logger.info(f"Email sent to {to_email} — subject: {subject}")

# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    # Load .env from project root
    project_root = Path(__file__).resolve().parent.parent.parent
    env_file = project_root / ".env"
    if env_file.exists():
        load_dotenv(env_file)
        logger.info(f"Loaded env from {env_file}")
    else:
        load_dotenv()

    # Required env vars
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    gmail_user = os.environ.get("GMAIL_USER", "").strip()
    gmail_password = os.environ.get("GMAIL_APP_PASSWORD", "").strip()
    recipient = os.environ.get("RECIPIENT_EMAIL", "nxbach1509@gmail.com").strip()

    # Optional
    tavily_key = os.environ.get("TAVILY_API_KEY", "").strip() or None

    missing = [
        name for name, val in [
            ("ANTHROPIC_API_KEY", anthropic_key),
            ("GMAIL_USER", gmail_user),
            ("GMAIL_APP_PASSWORD", gmail_password),
        ]
        if not val
    ]
    if missing:
        logger.error(f"Missing required env vars: {', '.join(missing)}")
        logger.error(f"Copy .env.example to .env and fill in the values.")
        sys.exit(1)

    week_info = get_week_info()
    logger.info(
        f"Generating AI Weekly — Tuần {week_info['week_num']}, "
        f"{week_info['date_range']}"
    )

    # Generate report
    try:
        report = generate_report(week_info, anthropic_key, tavily_key)
    except Exception as exc:
        logger.error(f"Report generation failed: {exc}", exc_info=True)
        sys.exit(1)

    # Save local copy
    report_path = LOG_DIR / f"ai_weekly_week{week_info['week_num']}_{week_info['year']}.txt"
    report_path.write_text(report, encoding="utf-8")
    logger.info(f"Report saved locally: {report_path}")

    # Build email subject
    subject = f"AI Weekly — Tuần {week_info['week_num']}, {week_info['friday_date']}"

    # Send email (retry up to 3 times)
    for attempt in range(1, 4):
        try:
            send_email(recipient, subject, report, gmail_user, gmail_password)
            break
        except Exception as exc:
            logger.warning(f"Email attempt {attempt} failed: {exc}")
            if attempt < 3:
                time.sleep(2 ** attempt)
            else:
                logger.error("All email attempts failed. Report saved locally.")
                sys.exit(1)

    logger.info("AI Weekly routine completed successfully.")


if __name__ == "__main__":
    main()
