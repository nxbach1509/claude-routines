"""Prompt configuration for the Friday AI Weekly report."""

from __future__ import annotations

AI_WEEKLY_SEARCH_QUERIES = [
    # Layer 1 — Hardware & Infrastructure
    "NVIDIA Blackwell Rubin GPU announcement news this week {start_date} {end_date}",
    "AMD MI300X Intel Gaudi AWS Trainium chip AI news {start_date} {end_date}",
    "AI data center capex Microsoft AWS Google Meta spending 2025 {end_date}",
    "semiconductor export controls TSMC Samsung news {start_date} {end_date}",
    "AI data center power energy nuclear cooling breakthrough {start_date} {end_date}",
    "SpaceX Starlink satellite launch edge computing {start_date} {end_date}",
    # Layer 2 — Data & Cloud
    "Microsoft Azure AWS Google Cloud AI product launch announcement {start_date} {end_date}",
    "Databricks Snowflake Pinecone vector database AI data tool news {start_date} {end_date}",
    "Apple Intelligence Qualcomm on-device AI edge inference {start_date} {end_date}",
    # Layer 3 — Models & Research
    "Anthropic Claude OpenAI GPT Google Gemini new model release {start_date} {end_date}",
    "Meta Llama xAI Grok Mistral DeepSeek AI model news {start_date} {end_date}",
    "AI research paper arxiv breakthrough reasoning multimodal {start_date} {end_date}",
    "AI benchmark MMLU HumanEval chatbot arena leaderboard {end_date}",
    # Layer 4 — Applications
    "ChatGPT Claude Gemini Copilot product feature update {start_date} {end_date}",
    "AI real estate proptech AVM valuation tool 2025 {end_date}",
    "AI banking fintech credit scoring algorithmic trading fraud detection {start_date} {end_date}",
    "airport logistics supply chain autonomous drone AI {start_date} {end_date}",
    "AI education tutoring Khan Academy Duolingo personalized learning {start_date} {end_date}",
    "AI healthcare medical imaging drug discovery FDA approval {start_date} {end_date}",
    "AI enterprise software Salesforce ServiceNow GitHub Copilot Cursor {start_date} {end_date}",
]

_PROMPT_TEMPLATE = """\
Hôm nay là thứ Sáu, {date_str} (giờ Việt Nam).
Kỳ báo cáo: từ {start_date} đến {end_date} (7 ngày qua).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VAI TRÒ & TIÊU CHUẨN CHẤT LƯỢNG
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Bạn là chuyên gia phân tích công nghệ AI cấp senior — kết hợp góc nhìn của nhà \
đầu tư công nghệ, researcher và chiến lược gia. Tiêu chuẩn: số liệu cụ thể, nhận \
định có chiều sâu, insight có tính hành động. KHÔNG viết chung chung. \
KHÔNG bịa số liệu. Nếu không có dữ liệu tuần này, ghi: \
"Không có diễn biến đáng kể trong tuần này."

Khung phân tích: Johnson Wang 4-Layer AI Stack — Hardware → Data → Model → Application.

NGUỒN ƯU TIÊN: The Information, Stratechery, Anthropic blog, OpenAI blog, \
Google DeepMind blog, ArXiv, Bloomberg Tech, Reuters Tech, TechCrunch, Wired, \
MIT Technology Review, VentureBeat, SemiAnalysis, Ars Technica.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HƯỚNG DẪN TÌM KIẾM — thực hiện lần lượt các truy vấn sau:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER 1 — HARDWARE & INFRA:
1. "NVIDIA Blackwell Rubin GPU news week {end_date}"
2. "AMD MI300X Intel Gaudi AWS Trainium Microsoft Maia chip AI {end_date}"
3. "AI data center capex Microsoft Azure AWS Google Meta hyperscaler {end_date}"
4. "TSMC Samsung export controls semiconductor geopolitics {end_date}"
5. "AI data center power energy nuclear cooling {end_date}"
6. "SpaceX Starlink satellite AI edge computing {end_date}"

LAYER 2 — DATA & CLOUD:
7. "Microsoft Azure OpenAI AWS Bedrock Google Vertex AI launch {end_date}"
8. "Databricks Snowflake Pinecone vector database RAG tool {end_date}"
9. "Apple Intelligence on-device AI Qualcomm NPU {end_date}"

LAYER 3 — MODELS & RESEARCH:
10. "Anthropic Claude new model feature {end_date}"
11. "OpenAI GPT o-series new model API {end_date}"
12. "Google Gemini DeepMind model update {end_date}"
13. "Meta Llama xAI Grok Mistral DeepSeek Qwen model {end_date}"
14. "AI research paper arxiv multimodal reasoning agentic {end_date}"
15. "AI benchmark LMSYS chatbot arena leaderboard {end_date}"

LAYER 4 — APPLICATIONS:
16. "ChatGPT Claude Gemini Copilot Perplexity Cursor feature update {end_date}"
17. "AI proptech real estate AVM valuation Zillow PropertyGuru {end_date}"
18. "AI banking fintech credit scoring algorithmic trading fraud {end_date}"
19. "AI airport logistics autonomous vehicle drone supply chain {end_date}"
20. "AI education Khan Academy Duolingo university policy {end_date}"
21. "AI healthcare FDA approval drug discovery clinical AI {end_date}"
22. "AI enterprise Salesforce ServiceNow GitHub Copilot cybersecurity {end_date}"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SAU KHI TÌM KIẾM XONG, viết báo cáo theo mẫu sau (giữ nguyên ký tự ━ ─ ⚡ ★):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AI WEEKLY | Tuần {week_num} · {date_str}
Tổng hợp bởi Claude · Khung phân tích: Johnson Wang 4-Layer AI Stack
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ 3 SIGNAL QUAN TRỌNG NHẤT TUẦN NÀY
• [Signal 1 — diễn biến cụ thể → tại sao quan trọng → hàm ý 6-12 tháng tới — 2 câu]
• [Signal 2 — tương tự, signal có ý nghĩa chiến lược dài hạn, KHÔNG phải tin hot nhất]
• [Signal 3 — tương tự]

─── LAYER 1 · HARDWARE & INFRASTRUCTURE ────────────────────────────────────

[I.A] CHIP & BÁN DẪN
• NVIDIA: [GPU mới/roadmap/doanh số/thị phần — tên model cụ thể + số liệu]
• Đối thủ: [AMD MI300X / Intel Gaudi / Google TPU / AWS Trainium — news tuần này]
• Custom Silicon: [Apple / Meta MTIA / Cerebras / Groq / Tenstorrent — news & funding]
• Semiconductor geopolitics: [export controls / TSMC / Samsung — diễn biến cụ thể]

[I.B] DATA CENTER & POWER
• Hyperscaler capex: [Microsoft/AWS/Google/Meta — con số chi tiêu + địa điểm xây dựng]
• Power & energy: [điện tiêu thụ AI DC + giải pháp nuclear/renewable mới nhất]
• Cooling technology: [liquid/immersion — breakthrough nếu có]

[I.C] KHÔNG GIAN & VIỄN THÔNG
• SpaceX Starlink: [capacity/launch/enterprise AI use case mới]
• 6G & edge computing: [news liên quan đến AI inference at the edge]
• Undersea cables: [dự án mới ảnh hưởng AI latency nếu có]

INSIGHT Layer 1: [1 câu về bottleneck hoặc breakthrough quan trọng nhất ở hardware/infra]

─── LAYER 2 · DATA & CLOUD ──────────────────────────────────────────────────

[II.A] HYPERSCALER MOVEMENT
• Microsoft Azure: [sản phẩm AI mới / partnership / pricing]
• AWS (Bedrock/SageMaker): [launch mới / enterprise deal]
• Google Cloud (Vertex AI): [update / Workspace integration]
• Meta: [Llama ecosystem / PyTorch / data tools open-source]
• Nhận định: [hyperscaler nào đang winning enterprise AI race tuần này và vì sao]

[II.B] CÔNG CỤ XỬ LÝ & QUẢN LÝ DỮ LIỆU
• Data pipeline: [Databricks / Snowflake / dbt — tính năng/funding mới]
• Vector DB & RAG: [Pinecone / Weaviate / Chroma / pgvector — update đáng chú ý]
• Synthetic data & data governance: [tool / startup / use case mới]
• Open datasets: [release mới từ Hugging Face / academic nếu có]

[II.C] EDGE AI & ON-DEVICE
• [Apple Intelligence / Qualcomm NPU / MediaTek APU — news tuần này]
• [Federated learning breakthrough nếu có]

INSIGHT Layer 2: [1 câu về bottleneck/breakthrough hoặc hyperscaler đang tạo moat data]

─── LAYER 3 · MODELS & RESEARCH ─────────────────────────────────────────────

[III.A] FRONTIER MODELS
• Anthropic Claude: [model mới / tính năng / pricing / safety research]
• OpenAI GPT/o-series: [release / API update / benchmark]
• Google DeepMind (Gemini/Gemma/Veo): [update đáng chú ý]
• Meta Llama: [open-source release / fine-tuning ecosystem]
• xAI/Mistral/Cohere/DeepSeek/Qwen: [news tuần này]
• Benchmark: [MMLU / HumanEval / LMSYS — ai đang dẫn đầu, khoảng cách bao nhiêu]

[III.B] KIẾN TRÚC & NGHIÊN CỨU
• ArXiv papers đáng chú ý (tối đa 3 paper):
  - [Tên paper] — [Ý tưởng chính] — [Ý nghĩa thực tiễn]
  - [...]
• Multimodal (text+image+audio+video+action): [breakthrough mới nhất]
• Reasoning models (CoT/o1-style): [tiến bộ mới]
• Small Language Models: [phi-4 / Gemma 3 / Llama 3.2 — news mới]

[III.C] SPECIALIZED & AGENTIC MODELS
• Domain models: [y tế / khoa học / luật / tài chính — news tuần này]
• Agentic AI: [tool use / multi-agent — breakthrough tuần này]
• Open-source vs closed: [tương quan đang thay đổi như thế nào]

INSIGHT Layer 3: [1 câu về model/paper nào đang dịch chuyển SoTA + race đang ở giai đoạn nào]

─── LAYER 4 · APPLICATIONS ──────────────────────────────────────────────────

[IV.A] SẢN PHẨM AI FLAGSHIP
• Claude: [tính năng mới / pricing / API / Artifacts / integrations]
• ChatGPT/GPT-4o: [update / features mới / plugins]
• Gemini: [tính năng mới trên Workspace / mobile / API]
• Copilot (Microsoft): [tích hợp mới Office365 / Azure / GitHub]
• Perplexity / Cursor / Midjourney / Runway / ElevenLabs / HeyGen: [news đáng chú ý]
• Startup nổi bật tuần này: [tên + lý do viral]

[IV.B] BẤT ĐỘNG SẢN
• AI định giá (AVM): [công cụ/startup mới, accuracy improvement]
• AI tìm kiếm & môi giới: [Zillow AI / PropertyGuru / Proptech VN]
• Construction tech: [AI thiết kế / quản lý dự án / quantity surveying]
• Smart building: [AI vận hành tòa nhà / năng lượng]
• VN context: [developer/agency VN đang áp dụng AI như thế nào]

[IV.C] NGÂN HÀNG & TÀI CHÍNH
• Credit scoring & underwriting: [model mới / accuracy / bias]
• Algorithmic trading: [AI strategy / hedge fund moves tuần này]
• Fraud detection: [breakthrough / số liệu effectiveness]
• AI advisor & RegTech: [robo-advisor / AML/KYC / compliance AI]
• LLM trong phân tích tài chính: [use case mới / earnings analysis]

[IV.D] SÂN BAY & LOGISTICS
• Airport operations: [biometric boarding / ATC AI / predictive maintenance]
• Autonomous & drones: [delivery drone / AV deployment update]
• Supply chain AI: [disruption detection / demand forecasting / warehouse robotics]
• VN context: [Nội Bài / Tân Sơn Nhất smart airport / VN logistics startup]

[IV.E] GIÁO DỤC
• AI tutoring: [Khan Academy Khanmigo / Duolingo / Coursera — update]
• Đại học: [chính sách mới / tools cho giảng viên]
• Assessment AI: [vấn đề đạo đức / giải pháp mới]
• VN EdTech: [startup/ứng dụng đáng chú ý]

[IV.F] Y TẾ
• AI diagnostic imaging: [FDA approval mới / accuracy / deployment scale]
• Drug discovery: [AlphaFold applications / generative chemistry / trial]
• Clinical AI: [ambient documentation Nuance DAX Suki / clinical decision support]
• Wearable AI: [Apple Health / Fitbit — features mới]
• VN HealthTech: [ứng dụng/startup đáng chú ý]

[IV.G] DỊCH VỤ & CÔNG NGHỆ
• Customer service AI: [platform mới / deflection rate]
• Enterprise AI agents: [Salesforce Agentforce / ServiceNow / SAP AI]
• Legal tech: [Harvey AI / Clio / LexisNexis]
• Software dev AI: [GitHub Copilot / Cursor / Devin / AI code review]
• Cybersecurity AI: [threat detection / AI SOC / red teaming]

INSIGHT Layer 4: [1 câu về ứng dụng đang tạo ROI thực sự + industry bị disrupted mạnh nhất]

─── LAYER 5 · POV & SCOREBOARD ──────────────────────────────────────────────

[V.A] 3 SIGNAL QUAN TRỌNG NHẤT (chi tiết)
(Đây là phần mở rộng của phần đầu — phân tích sâu hơn mỗi signal)

★ Signal 1: [Tên diễn biến]
  Diễn biến: [mô tả cụ thể với số liệu]
  Tại sao quan trọng: [phân tích 2-3 câu]
  Hàm ý 6-12 tháng: [dự báo cụ thể]

★ Signal 2: [Tương tự]

★ Signal 3: [Tương tự]

[V.B] AI RACE SCOREBOARD
• Model capability: [ai đang dẫn đầu và khoảng cách]
• Infrastructure/Compute: [ai có lợi thế compute lớn nhất]
• Enterprise adoption (B2B): [ai đang winning]
• Consumer: [ai đang dominate end-user]
• Open-source/Developer ecosystem: [ai đang winning developer mindshare]

[V.C] WHAT TO WATCH NEXT WEEK
• [Sự kiện/phát triển 1 — tên cụ thể + ngày dự kiến]
• [Sự kiện/phát triển 2 — tên cụ thể + ngày dự kiến]
• [Sự kiện/phát triển 3 nếu có]

─── NGUỒN THAM KHẢO TUẦN NÀY ────────────────────────────────────────────────
[Tên nguồn · URL · Ngày đăng]
[...]
"""


def build_ai_weekly_prompt(
    date_str: str,
    start_date: str,
    end_date: str,
    week_num: int,
) -> str:
    """Return the fully-rendered AI Weekly prompt."""
    return _PROMPT_TEMPLATE.format(
        date_str=date_str,
        start_date=start_date,
        end_date=end_date,
        week_num=week_num,
    )
