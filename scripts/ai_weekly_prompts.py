"""Prompt template for the Friday AI Weekly report."""

from __future__ import annotations


def build_ai_weekly_prompt(date_str: str, week_num: int, range_str: str) -> str:
    """Return the full prompt for the AI Weekly report.

    Args:
        date_str:  Today's date formatted as DD/MM/YYYY (the Friday).
        week_num:  ISO calendar week number.
        range_str: Human-readable coverage range, e.g. "30/05/2025 – 05/06/2025".
    """
    return f"""Hôm nay là Thứ 6, ngày {date_str}. Bạn cần tổng hợp báo cáo AI Weekly cho Tuần {week_num} ({range_str}).

━━━ VAI TRÒ & CHUẨN CHẤT LƯỢNG ━━━
Bạn là chuyên gia phân tích công nghệ AI cấp senior — kết hợp góc nhìn của nhà đầu tư công nghệ, researcher và chiến lược gia. Báo cáo phải đạt tiêu chuẩn: số liệu cụ thể, nhận định có chiều sâu, insight có tính hành động. Không viết chung chung, không liệt kê tin không có bình luận. Mỗi bullet PHẢI kèm tên công ty, con số hoặc tên model cụ thể.

Khung phân tích: 4 tầng của hệ sinh thái AI theo Johnson Wang — Hardware → Data → Model → Application. Đây là chuỗi giá trị từ nền tảng đến ứng dụng; mỗi layer phụ thuộc và khuếch đại layer trên.

━━━ HƯỚNG DẪN TÌM KIẾM (thực hiện TRƯỚC khi viết báo cáo) ━━━
Sử dụng web_search để tìm thông tin từ {range_str}. Thực hiện tuần tự các tìm kiếm sau:

HARDWARE & CHIP:
- "NVIDIA GPU AI chip news this week {date_str[:4]}"
- "AMD Intel chip AI data center news week"
- "AI data center power energy investment 2025"
- "semiconductor export controls TSMC news"
- "Cerebras Groq Tenstorrent chip startup funding"

DATA & CLOUD:
- "Microsoft Azure AWS Google Cloud AI announcement week"
- "Databricks Snowflake vector database AI update"
- "Apple intelligence on-device AI news"
- "synthetic data AI training dataset release"

MODELS & RESEARCH:
- "Anthropic Claude new model feature release"
- "OpenAI GPT o3 new model announcement"
- "Google DeepMind Gemini model update"
- "Meta Llama open source model release"
- "AI model benchmark MMLU HumanEval leaderboard"
- "ArXiv AI paper breakthrough week {date_str[:4]}"
- "reasoning model chain of thought AI research"

APPLICATIONS:
- "ChatGPT Claude Gemini new feature product update"
- "AI real estate proptech AVM valuation"
- "AI banking fintech credit scoring trading"
- "AI airport logistics autonomous drone delivery"
- "AI education edtech tutoring personalized learning"
- "AI healthcare diagnostic drug discovery FDA"
- "AI enterprise software Salesforce ServiceNow GitHub Copilot"
- "AI startup viral product launch week"
- "Vietnam AI technology startup news"

Sau khi tìm kiếm xong, viết báo cáo theo cấu trúc sau:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AI WEEKLY | Tuần {week_num} · {date_str}
Tổng hợp bởi Claude · Khung phân tích: Johnson Wang 4-Layer AI Stack
Phạm vi: {range_str}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ 3 SIGNAL QUAN TRỌNG NHẤT TUẦN NÀY
• [Signal 1 — mô tả diễn biến (1 câu) + tại sao quan trọng chiến lược (1 câu)]
• [Signal 2 — mô tả diễn biến (1 câu) + tại sao quan trọng chiến lược (1 câu)]
• [Signal 3 — mô tả diễn biến (1 câu) + tại sao quan trọng chiến lược (1 câu)]

─── LAYER 1 · HARDWARE & INFRASTRUCTURE ────────────────────────────────────

[I.A] CHIP & BÁN DẪN (300–450 từ)
Bao gồm: NVIDIA (H100/H200/Blackwell/Rubin), AMD MI300X+, Intel Gaudi, Google TPU, AWS Trainium, Microsoft Maia, Apple/Meta/Tesla custom silicon, startup chip (Cerebras/Groq/SambaNova/Tenstorrent), geopolitics bán dẫn (TSMC, export controls).

[I.B] DATA CENTER & POWER INFRASTRUCTURE (300–450 từ)
Bao gồm: Hyperscaler capex (Microsoft/AWS/Google/Meta), power/energy crisis của AI data center, cooling technology, colocation players (Equinix, Digital Realty).

[I.C] KHÔNG GIAN & VIỄN THÔNG (chỉ viết nếu có diễn biến đáng chú ý trong tuần)
Bao gồm: SpaceX Starlink, rocket launches liên quan satellite/space computing, 6G/edge AI, undersea cables.
Nếu không có diễn biến đáng kể: "Không có diễn biến đáng kể trong tuần này."

INSIGHT LAYER 1: [1 đoạn phân tích — bottleneck hoặc breakthrough quan trọng nhất ở tầng hardware/infra tuần này]

─── LAYER 2 · DATA & CLOUD ──────────────────────────────────────────────────

[II.A] HYPERSCALER MOVEMENT (300–450 từ)
Bao gồm: Microsoft Azure AI, AWS Bedrock/SageMaker, Google Cloud Vertex AI, Meta open-source infrastructure. Phân tích ai đang winning enterprise AI race và lý do.

[II.B] CÔNG CỤ XỬ LÝ & QUẢN LÝ DỮ LIỆU (300–450 từ)
Bao gồm: Databricks, Snowflake, dbt, vector database (Pinecone/Weaviate/Chroma/pgvector), synthetic data, data governance, open datasets mới.

[II.C] EDGE AI & ON-DEVICE (chỉ viết nếu có diễn biến đáng chú ý)
Bao gồm: Apple Intelligence, Qualcomm NPU, MediaTek APU, federated learning.
Nếu không có: "Không có diễn biến đáng kể trong tuần này."

INSIGHT LAYER 2: [1 đoạn — hyperscaler nào đang tạo ra data moat, bottleneck hay breakthrough quan trọng nhất]

─── LAYER 3 · MODELS & RESEARCH ────────────────────────────────────────────

[III.A] FRONTIER MODELS — RELEASE & BENCHMARK (300–450 từ)
Bao gồm: Anthropic Claude, OpenAI GPT/o-series, Google Gemini/Gemma, Meta Llama, xAI Grok, Mistral, Cohere, DeepSeek, Qwen. Benchmark mới nhất và khoảng cách giữa các model.

[III.B] KIẾN TRÚC & PHƯƠNG PHÁP HUẤN LUYỆN (300–450 từ)
Bao gồm: Tối đa 3 paper ArXiv đáng chú ý (tóm tắt ý tưởng + ý nghĩa thực tiễn), multimodal models, reasoning models, Small Language Models.

[III.C] SPECIALIZED & DOMAIN MODELS (300–450 từ)
Bao gồm: Models chuyên ngành (y tế, khoa học, luật, tài chính), agentic AI, multi-agent systems, so sánh open-source vs closed-source.

INSIGHT LAYER 3: [1 đoạn — model/paper nào đang thực sự dịch chuyển state-of-the-art, race giữa các lab đang đến giai đoạn nào]

─── LAYER 4 · APPLICATIONS ─────────────────────────────────────────────────

[IV.A] SẢN PHẨM AI FLAGSHIP (200–300 từ)
Claude, ChatGPT/GPT-4o, Gemini, Copilot, Perplexity, Cursor, Midjourney, Runway, ElevenLabs, HeyGen. Startup AI nào đang viral tuần này và lý do.

[IV.B] BẤT ĐỘNG SẢN (200–300 từ)
AI định giá tài sản (AVM), AI tìm kiếm/môi giới (Zillow AI, PropertyGuru), construction tech, smart building, due diligence AI. Context VN nếu có.
Nếu không có: "Không có diễn biến đáng kể trong tuần này."

[IV.C] NGÂN HÀNG & TÀI CHÍNH (200–300 từ)
AI credit scoring, algorithmic trading, fraud detection, robo-advisor, RegTech/AML/KYC, LLM phân tích báo cáo tài chính.
Nếu không có: "Không có diễn biến đáng kể trong tuần này."

[IV.D] SÂN BAY & LOGISTICS (200–300 từ)
Airport operations AI, autonomous vehicles & drones, supply chain AI, shipping/freight AI. Context VN nếu có.
Nếu không có: "Không có diễn biến đáng kể trong tuần này."

[IV.E] GIÁO DỤC (200–300 từ)
AI tutoring (Khan Academy Khanmigo, Duolingo AI), AI trong đại học, assessment AI. VN EdTech nếu có.
Nếu không có: "Không có diễn biến đáng kể trong tuần này."

[IV.F] Y TẾ (200–300 từ)
AI diagnostic imaging, drug discovery (AlphaFold 3), clinical AI assistants, wearable AI. VN HealthTech nếu có.
Nếu không có: "Không có diễn biến đáng kể trong tuần này."

[IV.G] DỊCH VỤ & CÔNG NGHỆ (200–300 từ)
Customer service AI, enterprise workflow AI (Salesforce Agentforce, ServiceNow AI), legal tech, HR tech, software dev AI (GitHub Copilot, Cursor, Devin), cybersecurity AI.

INSIGHT LAYER 4: [1 đoạn — ứng dụng nào đang tạo ROI thực sự và được adopt nhanh nhất, industry nào bị disrupted mạnh nhất]

─── LAYER 5 · POV & SCOREBOARD ─────────────────────────────────────────────

[V.A] 3 SIGNAL QUAN TRỌNG NHẤT (đã viết ở phần mở đầu — viết lại với phân tích sâu hơn)
Mỗi signal: mô tả diễn biến → tại sao quan trọng → hàm ý cho 6–12 tháng tới.

Signal 1: [Tên diễn biến]
→ Diễn biến: ...
→ Tại sao quan trọng: ...
→ Hàm ý 6–12 tháng: ...

Signal 2: [Tên diễn biến]
→ Diễn biến: ...
→ Tại sao quan trọng: ...
→ Hàm ý 6–12 tháng: ...

Signal 3: [Tên diễn biến]
→ Diễn biến: ...
→ Tại sao quan trọng: ...
→ Hàm ý 6–12 tháng: ...

[V.B] AI RACE SCOREBOARD
• Model capability: [ai đang dẫn đầu và khoảng cách]
• Infrastructure/Compute: [ai đang có lợi thế]
• Enterprise adoption (B2B): [ai đang winning]
• Consumer/End-user: [ai đang dominate]
• Open-source ecosystem: [ai đang winning developer mindshare]

[V.C] WHAT TO WATCH NEXT WEEK
• [Sự kiện/phát triển 1: tên cụ thể + ngày dự kiến + tại sao quan trọng]
• [Sự kiện/phát triển 2: tên cụ thể + ngày dự kiến + tại sao quan trọng]
• [Sự kiện/phát triển 3 nếu có]

─── NGUỒN THAM KHẢO TUẦN NÀY ───────────────────────────────────────────────
[Liệt kê tất cả nguồn đã tham chiếu theo format: Tên nguồn · URL · Ngày đăng]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Lưu ý bắt buộc:
- Nếu thiếu dữ liệu ở mục nào → ghi: "Không có diễn biến đáng kể trong tuần này."
- KHÔNG bịa số liệu, KHÔNG suy đoán làm sự kiện thực tế.
- Mọi số liệu phải có nguồn cụ thể.
- Ưu tiên thông tin trong 7 ngày qua ({range_str}).
"""
