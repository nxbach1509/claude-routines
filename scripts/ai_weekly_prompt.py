"""Prompt configuration for the AI Weekly report (every Friday)."""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Shared preamble
# ---------------------------------------------------------------------------
_PREAMBLE = """\
Hôm nay là {date_str} (giờ Việt Nam). Đây là tuần {week_num} năm {year}.
Phạm vi thời gian báo cáo: từ {start_date} đến {end_date} (7 ngày qua).

Bạn là chuyên gia phân tích công nghệ AI cấp senior — kết hợp góc nhìn của nhà đầu tư \
công nghệ, researcher và chiến lược gia.
Khung phân tích: 4 tầng hệ sinh thái AI theo Johnson Wang — Hardware → Data → Model → Application.

TIÊU CHUẨN ĐẦU RA:
• Mỗi bullet PHẢI có số liệu, tên công ty, tên model, hoặc ví dụ cụ thể.
• Nếu không có diễn biến đáng kể ở mục nào → ghi: "Không có diễn biến đáng kể trong tuần này."
• KHÔNG bịa số liệu, KHÔNG suy đoán làm sự kiện.
• Tổng độ dài: 1.500–2.000 từ. Mỗi phần (I–V): 300–450 từ.
• Ngôn ngữ: Tiếng Việt. Văn phong: chuyên nghiệp, súc tích, dùng bullet points.
• Ưu tiên thông tin trong 7 ngày qua (từ {start_date} đến {end_date}).

NGUỒN ƯU TIÊN (tìm kiếm 7 ngày qua trước):
The Information, Stratechery, AI Index (Stanford), Anthropic blog, OpenAI blog, \
Google DeepMind blog, ArXiv, Bloomberg Tech, Reuters Tech, TechCrunch, Wired, \
MIT Technology Review, VentureBeat, SemiAnalysis, Dylan Patel, SpaceNews, Ars Technica.\
"""

_SEARCH_INSTRUCTIONS = """\

HƯỚNG DẪN TÌM KIẾM — thực hiện lần lượt các cụm từ sau:
1. "NVIDIA GPU Blackwell Rubin announcement {week_ref}"
2. "AMD MI300X Intel Gaudi Google TPU AWS Trainium {week_ref}"
3. "AI data center power consumption hyperscaler capex {week_ref}"
4. "Microsoft Azure AWS Google Cloud AI new product {week_ref}"
5. "Databricks Snowflake vector database RAG update {week_ref}"
6. "Anthropic Claude new model release {week_ref}"
7. "OpenAI GPT o-series new release {week_ref}"
8. "Google Gemini DeepMind update {week_ref}"
9. "Meta Llama open source release {week_ref}"
10. "AI arxiv paper breakthrough {week_ref}"
11. "ChatGPT Claude Gemini Copilot new feature {week_ref}"
12. "AI real estate proptech AVM {week_ref}"
13. "AI banking fintech credit scoring fraud detection {week_ref}"
14. "AI airport logistics supply chain {week_ref}"
15. "AI education healthcare {week_ref}"\
"""

_REPORT_TEMPLATE = """\

SAU KHI TÌM KIẾM, viết báo cáo theo đúng mẫu sau (giữ nguyên ký tự ━ ─ ⚡):

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AI WEEKLY | Tuần {week_num} · {date_str}
Tổng hợp bởi Claude · Khung phân tích: Johnson Wang 4-Layer AI Stack
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ 3 SIGNAL QUAN TRỌNG NHẤT TUẦN NÀY
• [Signal 1 — diễn biến → tại sao quan trọng → hàm ý 6–12 tháng tới]
• [Signal 2 — tương tự]
• [Signal 3 — tương tự]

─── LAYER 1 · HARDWARE & INFRASTRUCTURE ────────────────────────────────────

[I.A] CHIP & BÁN DẪN
• NVIDIA: [GPU mới / roadmap / doanh số / thị phần — số liệu cụ thể]
• Đối thủ: [AMD MI300X+ / Intel Gaudi / Google TPU / AWS Trainium / Microsoft Maia — tin mới nhất]
• Custom Silicon: [Apple / Meta MTIA / Tesla Dojo / Qualcomm — ai đang làm được gì?]
• Startup chip: [Cerebras / Groq / SambaNova / Tenstorrent — news & funding tuần này]
• Geopolitics: [export controls / TSMC / Samsung — diễn biến mới nhất]

[I.B] DATA CENTER & POWER INFRASTRUCTURE
• Hyperscaler capex: [Microsoft / AWS / Google / Meta — spend bao nhiêu, build ở đâu?]
• Power crisis: [AI data center tiêu thụ điện — nuclear/renewable solutions mới nhất]
• Colocation: [Equinix / Digital Realty / NTT — expansion news]

[I.C] KHÔNG GIAN & VIỄN THÔNG
• [SpaceX Starlink / 6G / undersea cables — tin liên quan đến AI infrastructure]

💡 INSIGHT LAYER 1: [Bottleneck hoặc breakthrough quan trọng nhất ở hardware/infra layer tuần này]

─── LAYER 2 · DATA & CLOUD ──────────────────────────────────────────────────

[II.A] HYPERSCALER MOVEMENT
• Microsoft Azure AI: [sản phẩm mới / partnership / pricing]
• AWS (Bedrock/SageMaker): [launch mới / enterprise deal]
• Google Cloud (Vertex AI): [update mới / Workspace integration]
• Meta (Llama ecosystem / PyTorch / data tools): [news mới nhất]
• Chiến lược: [hyperscaler nào đang winning enterprise AI race tuần này và vì sao?]

[II.B] CÔNG CỤ DỮ LIỆU & INFRASTRUCTURE
• Data pipeline: [Databricks / Snowflake / dbt — tin mới]
• Vector DB & RAG: [Pinecone / Weaviate / Chroma / pgvector — update đáng chú ý]
• Synthetic data & governance: [tools / startups / use case mới nhất]

[II.C] EDGE AI & ON-DEVICE
• [Apple Intelligence / Qualcomm NPU / MediaTek APU — on-device AI news]

💡 INSIGHT LAYER 2: [Bottleneck hay breakthrough ở data layer? Hyperscaler nào đang tạo moat data?]

─── LAYER 3 · MODELS & RESEARCH ────────────────────────────────────────────

[III.A] FRONTIER MODELS — RELEASE & BENCHMARK
• Anthropic (Claude): [model mới / tính năng / safety research / pricing]
• OpenAI (GPT/o-series/Sora): [release mới / API update / benchmark]
• Google DeepMind (Gemini/Gemma/Veo): [update đáng chú ý]
• Meta (Llama): [open-source release / fine-tuning ecosystem]
• Others: [xAI Grok / Mistral / Cohere / Qwen / DeepSeek — news tuần này]
• Benchmark: [MMLU / HumanEval / LMSYS Chatbot Arena — ai dẫn đầu, khoảng cách?]

[III.B] KIẾN TRÚC & NGHIÊN CỨU
• ArXiv papers nổi bật (tối đa 3):
  - [Tên paper + ý tưởng chính + ý nghĩa thực tiễn]
  - [...]
  - [...]
• Multimodal / Reasoning / SLM: [breakthrough mới nhất trong tuần]

[III.C] SPECIALIZED & DOMAIN MODELS
• [Y tế / Khoa học / Pháp lý / Tài chính — model chuyên ngành đáng chú ý]
• Agentic AI: [tool use / multi-agent — breakthrough trong tuần]
• Open-source vs closed-source: [tương quan lực lượng đang thay đổi ra sao?]

💡 INSIGHT LAYER 3: [Model/paper nào đang thực sự dịch chuyển state-of-the-art? Race giữa các lab?]

─── LAYER 4 · APPLICATIONS ─────────────────────────────────────────────────

[IV.A] SẢN PHẨM AI FLAGSHIP
• Claude (Anthropic): [tính năng mới / pricing / API / integrations]
• ChatGPT/GPT-4o (OpenAI): [update tuần này / new features]
• Gemini (Google): [tính năng mới trên Workspace / mobile / API]
• Copilot (Microsoft): [tích hợp mới vào Office 365 / Azure / GitHub]
• Others: [Perplexity / Cursor / Midjourney / Runway / ElevenLabs / HeyGen]
• Startup viral tuần này: [tên + lý do viral]

[IV.B] BẤT ĐỘNG SẢN
• AI định giá (AVM): [công cụ/startup mới / accuracy cải thiện]
• AI môi giới & tìm kiếm: [Zillow AI / PropertyGuru AI / Proptech VN]
• Construction tech & Smart building: [AI thiết kế / quản lý dự án / facility management]
• Case study VN: [AI đang được developer/agency VN áp dụng như thế nào?]

[IV.C] NGÂN HÀNG & TÀI CHÍNH
• Credit scoring & underwriting: [model mới / accuracy / bias concerns]
• Algorithmic trading & quant: [AI strategy mới / hedge fund moves tuần này]
• Fraud detection: [breakthrough / số liệu effectiveness]
• RegTech: [compliance automation / AML-KYC AI update]
• LLM phân tích tài chính: [use case mới — earnings calls, báo cáo tài chính]

[IV.D] SÂN BAY & LOGISTICS
• Airport AI: [biometric boarding / baggage tracking / ATC AI / predictive maintenance]
• AV & drones: [delivery drone / autonomous vehicle deployment update]
• Supply chain AI: [disruption detection / warehouse robotics / port automation]
• VN context: [Nội Bài / Tân Sơn Nhất smart airport / VN logistics tech startups]

[IV.E] GIÁO DỤC
• AI tutoring: [Khan Academy Khanmigo / Duolingo AI / Coursera AI — update]
• Đại học & assessment: [chính sách mới / tools mới / vấn đề đạo đức AI]
• VN EdTech AI: [startup/ứng dụng đáng chú ý]

[IV.F] Y TẾ
• AI diagnostic imaging: [FDA approval mới / accuracy benchmark / deployment scale]
• Drug discovery: [AlphaFold 3 applications / generative chemistry]
• Clinical AI assistants: [Nuance DAX / Suki / clinical decision support]
• VN HealthTech AI: [ứng dụng/startup đáng chú ý]

[IV.G] DỊCH VỤ & CÔNG NGHỆ
• Customer service AI: [platform mới / deflection rate improvements]
• Enterprise AI agents: [Salesforce Agentforce / ServiceNow / SAP AI]
• Legal & HR tech AI: [Harvey AI / Clio / recruiting AI update]
• Dev tools AI: [GitHub Copilot / Cursor / Devin / code review AI]
• Cybersecurity AI: [threat detection / AI-powered SOC]

💡 INSIGHT LAYER 4: [Ứng dụng nào tạo ROI thực sự và được adopt nhanh nhất? Industry nào bị disrupted mạnh nhất?]

─── LAYER 5 · POV & SCOREBOARD ─────────────────────────────────────────────

[V.A] AI RACE SCOREBOARD (snapshot tại {date_str})
• Model capability: [ai đang dẫn đầu?]
• Infrastructure: [ai có lợi thế compute?]
• Enterprise adoption (B2B): [ai đang winning?]
• Consumer: [ai đang dominate end-user?]
• Open-source ecosystem: [ai đang winning developer mindshare?]

[V.B] WHAT TO WATCH NEXT WEEK
• [Sự kiện/phát triển 1 — conference / expected release / regulatory decision / earnings]
• [Sự kiện/phát triển 2]
• [Sự kiện/phát triển 3]

─── NGUỒN THAM KHẢO TUẦN NÀY ───────────────────────────────────────────────
[Tên nguồn · URL (nếu có) · Ngày đăng]
[...]
[...]\
"""

PROMPT_TEMPLATE = _PREAMBLE + _SEARCH_INSTRUCTIONS + _REPORT_TEMPLATE


def build_prompt(
    date_str: str,
    week_num: int,
    year: int,
    start_date: str,
    end_date: str,
    week_ref: str,
) -> str:
    """Return the fully-rendered prompt for the AI weekly report."""
    return PROMPT_TEMPLATE.format(
        date_str=date_str,
        week_num=week_num,
        year=year,
        start_date=start_date,
        end_date=end_date,
        week_ref=week_ref,
    )
