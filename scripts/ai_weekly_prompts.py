"""Prompt template for the weekly AI industry report."""

from __future__ import annotations

_PROMPT_TEMPLATE = """\
Hôm nay là thứ Sáu, {date_str} (giờ Việt Nam). Đây là báo cáo AI Weekly Tuần {week_num}.

Bạn là chuyên gia phân tích công nghệ AI cấp senior — kết hợp góc nhìn của nhà đầu tư \
công nghệ, researcher và chiến lược gia. Tiêu chuẩn: số liệu cụ thể, nhận định có chiều \
sâu, insight có tính hành động. KHÔNG viết chung chung, KHÔNG liệt kê tin không có bình \
luận. KHÔNG bịa số liệu.

Kỳ báo cáo: từ {date_from} đến {date_to} (7 ngày qua).

Khung phân tích: Johnson Wang 4-Layer AI Stack:
Hardware → Data → Model → Application

TIÊU CHUẨN ĐẦU RA:
• Mỗi bullet PHẢI có số liệu hoặc ví dụ cụ thể (tên công ty, con số, tên model).
• Nếu không có diễn biến đáng kể → ghi: "Không có diễn biến đáng kể trong tuần này."
• Tổng dài báo cáo: 1.500–2.000 từ. Mỗi phần (Layer 1–5) khoảng 300–450 từ.
• Ngôn ngữ: Tiếng Việt. Văn phong: chuyên nghiệp, súc tích.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HƯỚNG DẪN TÌM KIẾM — thực hiện LẦN LƯỢT từng cụm từ dưới đây:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER 1 — HARDWARE & INFRASTRUCTURE:
1. "NVIDIA GPU AI chip news {date_str} Blackwell Rubin roadmap"
2. "AMD MI300X Intel Gaudi Google TPU AWS Trainium chip AI {date_str}"
3. "AI data center hyperscaler capex Microsoft AWS Google Meta {date_str}"
4. "semiconductor export controls TSMC AI chip geopolitics {date_str}"
5. "AI data center power energy nuclear renewable {date_str}"
6. "Cerebras Groq SambaNova Tenstorrent chip startup news {date_str}"
7. "SpaceX Starlink satellite launch edge computing AI {date_str}"

LAYER 2 — DATA & CLOUD:
8. "Microsoft Azure AWS Google Cloud AI new product launch {date_str}"
9. "Databricks Snowflake dbt vector database RAG AI update {date_str}"
10. "synthetic data generation AI tools startup {date_str}"
11. "Apple Intelligence on-device AI Qualcomm NPU {date_str}"
12. "open dataset Hugging Face release AI {date_str}"

LAYER 3 — MODELS & RESEARCH:
13. "Anthropic Claude model release update {date_str}"
14. "OpenAI GPT o-series Sora new release benchmark {date_str}"
15. "Google DeepMind Gemini Gemma Veo update {date_str}"
16. "Meta Llama open source model release {date_str}"
17. "DeepSeek Mistral Qwen xAI Grok model news {date_str}"
18. "AI arxiv paper reasoning multimodal breakthrough {date_str}"
19. "LMSYS Chatbot Arena benchmark leaderboard {date_str}"
20. "agentic AI multi-agent system tool use breakthrough {date_str}"

LAYER 4 — APPLICATIONS:
21. "ChatGPT Claude Gemini Copilot new feature update {date_str}"
22. "AI real estate proptech AVM property valuation {date_str}"
23. "AI banking fintech credit scoring fraud detection {date_str}"
24. "AI airport logistics autonomous vehicle drone {date_str}"
25. "AI education edtech personalized learning {date_str}"
26. "AI healthcare medical imaging drug discovery FDA approval {date_str}"
27. "GitHub Copilot Cursor Devin AI coding update {date_str}"
28. "AI customer service enterprise workflow Salesforce ServiceNow {date_str}"
29. "AI startup viral product launch funding {date_str}"

SAU KHI HOÀN THÀNH TÌM KIẾM, viết báo cáo theo đúng mẫu sau \
(giữ nguyên ký tự ━ ─ ⚡):

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AI WEEKLY | Tuần {week_num} · {date_str}
Tổng hợp bởi Claude · Khung phân tích: Johnson Wang 4-Layer AI Stack
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ 3 SIGNAL QUAN TRỌNG NHẤT TUẦN NÀY
• [Signal 1: mô tả diễn biến → tại sao quan trọng → hàm ý 6–12 tháng tới — 2 câu]
• [Signal 2: tương tự — 2 câu]
• [Signal 3: tương tự — 2 câu]

─── LAYER 1 · HARDWARE & INFRASTRUCTURE ────────────────────────────

[I.A] CHIP & BÁN DẪN
• NVIDIA: [GPU mới / roadmap / doanh số / so sánh Blackwell vs Rubin — phải có số liệu]
• Đối thủ: [AMD MI300X+ / Intel Gaudi / Google TPU / AWS Trainium / Microsoft Maia — \
news tuần này]
• Custom Silicon: [Apple / Meta MTIA / Tesla Dojo / Qualcomm — tin đáng chú ý]
• Startup chip: [Cerebras / Groq / SambaNova / Tenstorrent — news & funding tuần này]
• Semiconductor geopolitics: [export controls / TSMC / Samsung / Intel Foundry — \
diễn biến mới nhất]

[I.B] DATA CENTER & POWER INFRASTRUCTURE
• Hyperscaler capex: [Microsoft/AWS/Google/Meta đang spend bao nhiêu, build ở đâu?]
• Power: [AI data center tiêu thụ điện — nuclear/renewable solution mới nhất]
• Liquid cooling / immersion cooling: [breakthrough tuần này nếu có]

[I.C] KHÔNG GIAN & VIỄN THÔNG
• SpaceX Starlink: [capacity mới / enterprise AI use case]
• Satellite/space launch liên quan đến AI: [tin đáng chú ý nếu có]
• Edge computing & 6G: [liên kết với AI inference at the edge]

INSIGHT Layer 1: [Điều gì ở hardware/infra đang tạo ra bottleneck hoặc \
breakthrough quan trọng nhất cho AI toàn cầu tuần này? — 3–4 câu có số liệu]

─── LAYER 2 · DATA & CLOUD ──────────────────────────────────────────

[II.A] HYPERSCALER MOVEMENT
• Microsoft Azure AI: [sản phẩm mới / partnership / pricing thay đổi]
• AWS (Bedrock/SageMaker): [launch mới / enterprise deal đáng chú ý]
• Google Cloud (Vertex AI): [update / Workspace AI integration]
• Meta (open-source infra): [Llama ecosystem / PyTorch / data tools]
• Nhận định: [Hyperscaler nào đang winning enterprise AI race tuần này và vì sao?]

[II.B] CÔNG CỤ DỮ LIỆU & RAG INFRASTRUCTURE
• Data pipeline: [Databricks / Snowflake / dbt — tin tức/tính năng mới]
• Vector DB: [Pinecone / Weaviate / Chroma / pgvector — update đáng chú ý]
• Synthetic data & open datasets: [tools / startups / Hugging Face release mới nhất]

[II.C] EDGE AI & ON-DEVICE
• Apple Intelligence / Qualcomm NPU / MediaTek APU: [news tuần này]
• Federated learning: [breakthrough nếu có]

INSIGHT Layer 2: [Data layer đang có bottleneck hay breakthrough gì? \
Hyperscaler nào đang tạo ra moat data đáng kể? — 3–4 câu]

─── LAYER 3 · MODELS & RESEARCH ─────────────────────────────────────

[III.A] FRONTIER MODELS — RELEASE & BENCHMARK
• Anthropic (Claude): [model mới / tính năng / safety research / pricing]
• OpenAI (GPT/o-series/Sora): [release mới / API update / benchmark]
• Google DeepMind (Gemini/Gemma/Veo): [update đáng chú ý]
• Meta (Llama): [open-source release mới / fine-tuning ecosystem]
• Khác (xAI Grok / Mistral / Cohere / DeepSeek / Qwen): [news tuần này]
• Benchmark: [LMSYS Chatbot Arena / MMLU / HumanEval — ai đang dẫn đầu và khoảng cách]

[III.B] KIẾN TRÚC & NGHIÊN CỨU
• ArXiv papers đáng chú ý (tối đa 3): [tên paper + ý tưởng chính + ý nghĩa thực tiễn]
• Multimodal (text+image+audio+video): [breakthrough mới nhất]
• Reasoning models (Chain-of-Thought / o1-style): [tiến bộ tuần này]
• Small Language Models (SLM): [phi-4 / Gemma 3 / Llama 3.2 — news mới]

[III.C] SPECIALIZED & AGENTIC MODELS
• Domain models: [y tế Med-Gemini / khoa học AlphaFold / luật / tài chính — tin mới]
• Agentic AI: [tool use / multi-agent — breakthrough tuần này]
• Open-source vs closed-source: [tương quan lực lượng đang thay đổi như thế nào?]

INSIGHT Layer 3: [Model nào / paper nào đang thực sự dịch chuyển state-of-the-art? \
Race giữa các lab đang đến giai đoạn nào? — 3–4 câu]

─── LAYER 4 · APPLICATIONS ──────────────────────────────────────────

[IV.A] SẢN PHẨM AI FLAGSHIP
• Claude (Anthropic): [tính năng mới / pricing / API update / integrations]
• ChatGPT/GPT-4o (OpenAI): [update tuần này / features mới / tools]
• Gemini (Google): [tính năng mới trên Workspace / mobile / API]
• Copilot (Microsoft): [tích hợp mới vào Office 365 / Azure / GitHub]
• Perplexity / Cursor / Midjourney / Runway / ElevenLabs / HeyGen: [news đáng chú ý]
• Công cụ AI mới nổi viral trong tuần: [startup nào đang hot, tại sao?]

[IV.B] BẤT ĐỘNG SẢN
• AI định giá (AVM): [công cụ/startup mới / accuracy cải thiện]
• AI môi giới & tìm kiếm: [Zillow AI / PropertyGuru AI / Proptech VN]
• Construction tech: [AI trong thiết kế / quản lý dự án]
• Smart building: [AI vận hành tòa nhà / năng lượng]
• Case study VN: [AI đang được developer/agency VN áp dụng như thế nào?]

[IV.C] NGÂN HÀNG & TÀI CHÍNH
• Credit scoring & underwriting: [model mới / accuracy / bias concerns]
• Algorithmic trading & quant: [AI strategy mới / hedge fund AI moves]
• Fraud detection: [breakthrough / effectiveness]
• AI financial advisor: [Betterment / Wealthfront / VN fintechs update]
• LLM trong phân tích tài chính: [earnings call analysis / use case mới]

[IV.D] SÂN BAY & LOGISTICS
• Airport AI: [biometric boarding / baggage / ATC AI / predictive maintenance]
• Autonomous vehicles & drones: [delivery drone / AV deployment]
• Supply chain AI: [disruption detection / warehouse robotics]
• VN context: [Noi Bai / Tan Son Nhat smart airport; VN logistics tech]

[IV.E] GIÁO DỤC
• AI tutoring: [Khan Academy / Duolingo / Coursera AI update]
• AI trong đại học: [chính sách trường top / tools cho giảng viên]
• Assessment AI: [vấn đề đạo đức / giải pháp mới]
• VN EdTech AI: [startup/ứng dụng đáng chú ý]

[IV.F] Y TẾ
• AI diagnostic imaging: [FDA approval mới / accuracy / deployment scale]
• Drug discovery: [AlphaFold 3 applications / generative chemistry]
• Clinical AI: [Nuance DAX / Suki / clinical decision support]
• Wearable AI: [Apple Health / Fitbit AI features mới]
• VN HealthTech AI: [ứng dụng/startup đáng chú ý]

[IV.G] DỊCH VỤ & CÔNG NGHỆ
• Customer service AI: [platform mới / deflection rate]
• Enterprise AI agents: [Salesforce Agentforce / ServiceNow / SAP AI]
• Legal tech AI: [Harvey AI / Clio / LexisNexis AI]
• Software dev AI: [GitHub Copilot / Cursor / Devin / AI code review]
• Cybersecurity AI: [threat detection / AI-powered SOC]

INSIGHT Layer 4: [Ứng dụng nào đang tạo ra ROI thực sự và được adopt nhanh nhất? \
Industry nào đang bị disrupted mạnh nhất bởi AI tuần này? — 3–4 câu]

─── LAYER 5 · POV & SCOREBOARD ──────────────────────────────────────

[V.A] 3 SIGNAL QUAN TRỌNG NHẤT TUẦN NÀY
(Đây là phần tổng hợp chi tiết hơn cho phần ⚡ đã viết ở đầu — mở rộng mỗi signal \
thành 4–5 câu phân tích chiều sâu)
• Signal 1: [diễn biến → tại sao quan trọng chiến lược dài hạn → hàm ý 6–12 tháng]
• Signal 2: [tương tự]
• Signal 3: [tương tự]

[V.B] AI RACE SCOREBOARD
Snapshot tương quan lực lượng tại thời điểm này:
• Model capability: [ai đang dẫn đầu? khoảng cách với nhau?]
• Infrastructure/Compute: [ai đang có lợi thế compute?]
• Enterprise adoption: [ai đang winning B2B?]
• Consumer: [ai đang dominate end-user?]
• Open-source ecosystem: [ai đang winning developer mindshare?]

[V.C] WHAT TO WATCH NEXT WEEK
• [Sự kiện/phát triển 1: tên + ngày + tại sao quan trọng]
• [Sự kiện/phát triển 2: tương tự]
• [Sự kiện/phát triển 3: tương tự nếu có]

─── NGUỒN THAM KHẢO TUẦN NÀY ───────────────────────────────────────
[Tên nguồn · link · ngày đăng — liệt kê TẤT CẢ nguồn đã sử dụng]
"""


def build_ai_weekly_prompt(date_str: str, week_num: int, date_from: str, date_to: str) -> str:
    """Return the rendered AI Weekly prompt."""
    return _PROMPT_TEMPLATE.format(
        date_str=date_str,
        week_num=week_num,
        date_from=date_from,
        date_to=date_to,
    )
