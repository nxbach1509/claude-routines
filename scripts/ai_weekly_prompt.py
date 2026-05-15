"""Prompt configuration for the AI Weekly Friday report."""

from __future__ import annotations

AI_WEEKLY_PROMPT_TEMPLATE = """\
Hôm nay là thứ 6, {date_str} (giờ Việt Nam). Kỳ báo cáo: {period_start} – {period_end}.

Bạn là chuyên gia phân tích công nghệ AI cấp senior — kết hợp góc nhìn của nhà đầu tư \
công nghệ, researcher và chiến lược gia. Báo cáo phải đạt tiêu chuẩn: số liệu cụ thể, \
nhận định có chiều sâu, insight có tính hành động. KHÔNG viết chung chung, KHÔNG liệt kê \
tin không có bình luận.

Khung phân tích: 4 tầng của hệ sinh thái AI theo Johnson Wang — Hardware → Data → \
Model → Application.

TIÊU CHUẨN ĐẦU RA:
• Mỗi bullet PHẢI có tên công ty, con số hoặc tên model cụ thể.
• Nếu không có diễn biến đáng kể → ghi: "Không có diễn biến đáng kể trong tuần này."
• KHÔNG bịa số liệu, KHÔNG suy đoán làm sự kiện.
• Tổng dài: 1.500–2.000 từ. Mỗi layer 300–450 từ.
• Ngôn ngữ: Tiếng Việt. Văn phong chuyên nghiệp, súc tích.

NGUỒN ƯU TIÊN (tìm kiếm từ 7 ngày qua):
The Information, Stratechery, AI Index Stanford, Anthropic blog, OpenAI blog, \
Google DeepMind blog, ArXiv, Bloomberg Tech, Reuters Tech, TechCrunch, Wired, \
MIT Technology Review, VentureBeat, SemiAnalysis, Dylan Patel, SpaceNews, Ars Technica.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HƯỚNG DẪN TÌM KIẾM (thực hiện theo thứ tự, mỗi nhóm 2–3 queries):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[LAYER 1 — HARDWARE]
1. "NVIDIA Blackwell Rubin GPU news {date_str} 2025"
2. "AMD MI300X Intel Gaudi AWS Trainium AI chip news this week"
3. "TSMC Samsung Intel Foundry semiconductor export control news May 2025"
4. "AI data center hyperscaler capex Microsoft Google AWS Meta 2025"
5. "nuclear power AI data center electricity 2025"
6. "Cerebras Groq SambaNova Tenstorrent funding news 2025"

[LAYER 2 — DATA & CLOUD]
7. "Microsoft Azure AWS Google Cloud AI announcement this week May 2025"
8. "Databricks Snowflake vector database RAG AI announcement 2025"
9. "synthetic data federated learning privacy ML news 2025"
10. "Apple Intelligence Qualcomm NPU on-device AI news 2025"

[LAYER 3 — MODELS]
11. "Anthropic Claude new model release May 2025"
12. "OpenAI GPT o-series new release benchmark May 2025"
13. "Google Gemini DeepMind new model 2025"
14. "Meta Llama open source model release 2025"
15. "DeepSeek Mistral Qwen xAI Grok model news 2025"
16. "AI model benchmark MMLU HumanEval LMSYS Chatbot Arena leaderboard 2025"
17. "ArXiv AI paper reasoning multimodal agent breakthrough this week May 2025"

[LAYER 4 — APPLICATIONS]
18. "ChatGPT Claude Gemini Copilot new feature update May 2025"
19. "AI real estate proptech AVM automated valuation 2025"
20. "AI banking fintech credit scoring fraud detection algorithmic trading 2025"
21. "airport AI logistics autonomous vehicle drone delivery 2025"
22. "AI education tutoring personalized learning EdTech 2025"
23. "AI healthcare diagnostic imaging drug discovery clinical 2025"
24. "AI customer service enterprise workflow GitHub Copilot Cursor 2025"
25. "AI startup viral trending tool product launch this week 2025"

SAU KHI HOÀN THÀNH TÌM KIẾM, viết báo cáo theo đúng mẫu sau \
(giữ nguyên ký tự ━ ─ ⚡):

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AI WEEKLY | Tuần {week_num} · {date_str}
Tổng hợp bởi Claude · Khung phân tích: Johnson Wang 4-Layer AI Stack
Kỳ báo cáo: {period_start} – {period_end}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ 3 SIGNAL QUAN TRỌNG NHẤT TUẦN NÀY
• [Signal 1: mô tả diễn biến cụ thể + tên công ty/model → tại sao quan trọng về mặt chiến lược dài hạn]
• [Signal 2: tương tự — chọn signal khác layer hoặc góc nhìn]
• [Signal 3: tương tự]

─── LAYER 1 · HARDWARE & INFRASTRUCTURE ─────────────────────────────────────

[I.A] CHIP & BÁN DẪN
• NVIDIA: [GPU roadmap / doanh số / ra mắt mới — số liệu cụ thể, so sánh Blackwell vs Rubin nếu có tin mới]
• Đối thủ: [AMD MI300X+ / Intel Gaudi / Google TPU / AWS Trainium / Microsoft Maia — diễn biến nổi bật nhất]
• Custom Silicon: [Apple / Meta MTIA / Tesla Dojo / Qualcomm — ai đang làm gì mới?]
• Startup chip: [Cerebras / Groq / SambaNova / Tenstorrent — news & funding tuần này]
• Geopolitics bán dẫn: [export controls / TSMC / Samsung / Intel Foundry — diễn biến mới nhất]

[I.B] DATA CENTER & POWER
• Hyperscaler capex: [Microsoft/AWS/Google/Meta đang chi bao nhiêu, build ở đâu — số liệu cụ thể]
• Power crisis: [AI data center tiêu thụ điện + nuclear/renewable solutions mới nhất]
• Công nghệ làm mát / colocation: [liquid cooling / immersion / Equinix / Digital Realty — nếu có tin]

[I.C] KHÔNG GIAN & VIỄN THÔNG
• [SpaceX Starlink / satellite internet / 6G edge AI / undersea cable — tin đáng chú ý nếu có]

INSIGHT LAYER 1: [Hardware/infra layer đang tạo ra bottleneck hay breakthrough quan trọng nhất cho AI toàn cầu tuần này — 2–3 câu có số liệu]

─── LAYER 2 · DATA & CLOUD ──────────────────────────────────────────────────

[II.A] HYPERSCALER MOVEMENT
• Microsoft Azure AI: [sản phẩm mới / partnership / pricing]
• AWS Bedrock/SageMaker: [launch mới / enterprise deal]
• Google Cloud Vertex AI: [update / Workspace integration]
• Meta AI infrastructure: [Llama ecosystem / PyTorch / data tools]
• Nhận định: [hyperscaler nào đang winning enterprise AI race tuần này và vì sao]

[II.B] CÔNG CỤ XỬ LÝ & QUẢN LÝ DỮ LIỆU
• Data pipeline/orchestration: [Databricks / Snowflake / dbt — news tuần này]
• Vector DB & RAG: [Pinecone / Weaviate / Chroma / pgvector — update đáng chú ý]
• Synthetic data / governance: [tools / startups / use case mới]
• Open datasets: [Hugging Face / Common Crawl / academic release mới]

[II.C] EDGE AI & ON-DEVICE
• [Apple Intelligence / Qualcomm NPU / MediaTek APU — on-device AI news]
• [Federated learning / privacy-preserving ML — breakthrough nếu có]

INSIGHT LAYER 2: [Data layer bottleneck hay breakthrough quan trọng nhất — hyperscaler nào đang tạo ra moat data đáng kể — 2–3 câu]

─── LAYER 3 · MODELS & RESEARCH ─────────────────────────────────────────────

[III.A] FRONTIER MODELS
• Anthropic Claude: [model mới / tính năng / safety research / pricing — tuần này]
• OpenAI GPT/o-series/Sora: [release / API update / benchmark]
• Google DeepMind Gemini/Gemma/Veo: [update đáng chú ý]
• Meta Llama: [open-source release / fine-tuning ecosystem]
• xAI Grok / Mistral / Cohere / Qwen / DeepSeek: [news tuần này]
• Benchmark: [MMLU / HumanEval / LMSYS Chatbot Arena — ai đang dẫn đầu, khoảng cách]

[III.B] KIẾN TRÚC & TRAINING
• ArXiv papers đáng chú ý (tối đa 3):
  - Paper 1: [tên + tác giả/lab + ý tưởng chính + ý nghĩa thực tiễn]
  - Paper 2: [tương tự]
  - Paper 3: [tương tự, nếu có]
• Multimodal: [text+image+audio+video+action — breakthrough mới nhất]
• Reasoning models: [Chain-of-Thought / o1-style — tiến bộ mới]
• SLM & compression: [phi-4 / Gemma 3 / Llama 3.2 — news]

[III.C] SPECIALIZED & AGENTIC MODELS
• Domain models: [Med-Gemini / AlphaFold / legal / finance AI — đáng chú ý tuần này]
• Agentic AI: [tool use / multi-agent systems — breakthrough]
• Open-source vs closed: [tương quan lực lượng đang thay đổi như thế nào?]

INSIGHT LAYER 3: [Model/paper nào đang dịch chuyển state-of-the-art thực sự? Race giữa các lab đến giai đoạn nào? — 2–3 câu]

─── LAYER 4 · APPLICATIONS ──────────────────────────────────────────────────

[IV.A] SẢN PHẨM AI FLAGSHIP
• Claude: [tính năng mới / pricing / API / integrations]
• ChatGPT/GPT-4o: [update / new features / plugins]
• Gemini: [Workspace / mobile / API updates]
• Copilot: [Office 365 / Azure / GitHub integrations]
• Nổi bật: [Perplexity / Cursor / Midjourney / Runway / ElevenLabs / HeyGen — news]
• Viral mới: [startup/tool nào đang viral tuần này và tại sao]

[IV.B] BẤT ĐỘNG SẢN
• AI định giá (AVM): [công cụ/startup mới, accuracy cải thiện — số liệu]
• AI tìm kiếm & môi giới: [Zillow AI / PropertyGuru / Proptech VN]
• Construction tech: [AI thiết kế / quản lý dự án / quantity surveying]
• Smart building: [AI vận hành tòa nhà, năng lượng]
• VN context: [developer/agency VN áp dụng AI như thế nào]

[IV.C] NGÂN HÀNG & TÀI CHÍNH
• Credit scoring/underwriting: [model mới / accuracy / bias]
• Algorithmic trading/quant: [AI strategy / hedge fund AI tuần này]
• Fraud detection: [breakthrough / số liệu effectiveness]
• Robo-advisor: [Betterment / Wealthfront / VN fintechs]
• RegTech/LLM: [compliance / AML/KYC / phân tích báo cáo tài chính]

[IV.D] SÂN BAY & LOGISTICS
• Airport operations AI: [biometric / baggage / ATC / predictive maintenance]
• Autonomous vehicles/drones: [delivery drone / AV deployment]
• Supply chain AI: [disruption detection / demand forecasting / warehouse robotics]
• VN context: [Nội Bài / Tân Sơn Nhất / VN logistics tech]

[IV.E] GIÁO DỤC
• AI tutoring: [Khan Academy Khanmigo / Duolingo / Coursera AI — update]
• AI trong giảng dạy: [chính sách trường top / tools cho giảng viên]
• VN EdTech AI: [startup/ứng dụng đáng chú ý]

[IV.F] Y TẾ
• AI diagnostic imaging: [FDA approval mới / accuracy benchmark]
• Drug discovery: [AlphaFold 3 / generative chemistry / trial results]
• Clinical AI: [Nuance DAX / Suki / clinical decision support]
• VN HealthTech: [ứng dụng/startup đáng chú ý]

[IV.G] DỊCH VỤ & CÔNG NGHỆ
• Customer service AI: [conversational AI / deflection rate]
• Enterprise AI agents: [Salesforce Agentforce / ServiceNow / SAP AI]
• Legal tech: [Harvey AI / Clio / LexisNexis — contract review]
• Software dev AI: [GitHub Copilot / Cursor / Devin / AI code review]
• Cybersecurity AI: [threat detection / AI SOC / red teaming]

INSIGHT LAYER 4: [Ứng dụng nào đang tạo ROI thực sự và được adopt nhanh nhất? Industry nào bị disrupted mạnh nhất tuần này? — 2–3 câu]

─── LAYER 5 · POV & SCOREBOARD ──────────────────────────────────────────────

[V.A] 3 SIGNAL QUAN TRỌNG NHẤT (chi tiết hơn phần mở đầu)
1. [Signal 1] Diễn biến: [...] → Tại sao quan trọng: [...] → Hàm ý 6–12 tháng: [...]
2. [Signal 2] Diễn biến: [...] → Tại sao quan trọng: [...] → Hàm ý 6–12 tháng: [...]
3. [Signal 3] Diễn biến: [...] → Tại sao quan trọng: [...] → Hàm ý 6–12 tháng: [...]

[V.B] AI RACE SCOREBOARD (snapshot tại {date_str})
• Model capability: [ai đang dẫn đầu — tên model + bằng chứng benchmark]
• Infrastructure/Compute: [ai có lợi thế compute — số liệu capex/GPU]
• Enterprise adoption (B2B): [ai đang winning enterprise]
• Consumer: [ai đang dominate end-user]
• Open-source ecosystem: [ai đang winning developer mindshare]

[V.C] WHAT TO WATCH NEXT WEEK
• [Sự kiện/phát triển 1: conference / expected release / regulatory decision / earnings]
• [Sự kiện/phát triển 2]
• [Sự kiện/phát triển 3 nếu có]

─── NGUỒN THAM KHẢO TUẦN NÀY ────────────────────────────────────────────────
[Tên nguồn · URL (nếu có) · Ngày đăng]
"""


def build_ai_weekly_prompt(
    date_str: str,
    week_num: int,
    period_start: str,
    period_end: str,
) -> str:
    """Return the fully-rendered AI Weekly prompt."""
    return AI_WEEKLY_PROMPT_TEMPLATE.format(
        date_str=date_str,
        week_num=week_num,
        period_start=period_start,
        period_end=period_end,
    )
