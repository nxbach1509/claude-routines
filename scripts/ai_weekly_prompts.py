"""AI Weekly report prompt — Johnson Wang 4-Layer AI Stack."""

from __future__ import annotations

_PROMPT_TEMPLATE = """\
Hôm nay là thứ Sáu, {date_str} (giờ Việt Nam).
Kỳ báo cáo: từ {date_from} đến {date_to} (7 ngày qua).

Bạn là chuyên gia phân tích công nghệ AI cấp senior — kết hợp góc nhìn của nhà đầu tư \
công nghệ, researcher và chiến lược gia. Báo cáo phải đạt tiêu chuẩn: số liệu cụ thể, \
nhận định có chiều sâu, insight có tính hành động. Không viết chung chung, không liệt kê \
tin không có bình luận.

Khung phân tích: 4 tầng của hệ sinh thái AI theo Johnson Wang — \
Hardware → Data → Model → Application. Mỗi layer phụ thuộc và khuếch đại layer trên.

TIÊU CHUẨN ĐẦU RA:
• Mỗi bullet PHẢI có số liệu hoặc ví dụ cụ thể (tên công ty, con số, tên model).
• Nếu không có tin đáng kể trong 7 ngày qua → ghi: "Không có diễn biến đáng kể trong tuần này."
• KHÔNG bịa số liệu, không suy đoán làm sự kiện thật.
• Tổng độ dài báo cáo: 1.500–2.000 từ. Mỗi phần (Layer 1–4) 300–450 từ.
• Ngôn ngữ: Tiếng Việt. Văn phong chuyên nghiệp, súc tích, dùng bullet points.

NGUỒN ƯU TIÊN: The Information, Stratechery, Anthropic blog, OpenAI blog, Google DeepMind \
blog, ArXiv, Bloomberg Tech, Reuters Tech, TechCrunch, Wired, MIT Technology Review, \
VentureBeat, SemiAnalysis, Ars Technica, Stanford AI Index.

══════════════════════════════════════════════════════════════════════════════════
HƯỚNG DẪN TÌM KIẾM — thực hiện lần lượt từng truy vấn dưới đây trước khi viết báo cáo:
══════════════════════════════════════════════════════════════════════════════════

LAYER 1 — HARDWARE & INFRASTRUCTURE:
1. "NVIDIA Blackwell Rubin GPU news this week {date_str}"
2. "AMD MI300X Intel Gaudi Google TPU AWS Trainium AI chip news 2026"
3. "AI data center hyperscaler capex Microsoft Google AWS Meta spending 2026"
4. "AI data center power electricity nuclear renewable cooling 2026"
5. "SpaceX Starlink rocket launch satellite news this week 2026"
6. "TSMC Intel Foundry Samsung semiconductor export controls geopolitics 2026"
7. "Cerebras Groq SambaNova Tenstorrent AI chip startup funding 2026"

LAYER 2 — DATA & CLOUD:
8. "Microsoft Azure AI new features launch {date_str} 2026"
9. "AWS Amazon Bedrock SageMaker new product enterprise deal 2026"
10. "Google Cloud Vertex AI Workspace AI update 2026"
11. "Databricks Snowflake dbt data pipeline update 2026"
12. "Pinecone Weaviate vector database RAG infrastructure update 2026"
13. "Apple Intelligence Qualcomm NPU on-device AI news 2026"
14. "synthetic data generation federated learning privacy AI 2026"

LAYER 3 — MODELS & RESEARCH:
15. "Anthropic Claude new model feature release {date_str} 2026"
16. "OpenAI GPT o-series Sora new release API update benchmark 2026"
17. "Google DeepMind Gemini Gemma Veo update 2026"
18. "Meta Llama open source model release fine-tuning 2026"
19. "xAI Grok Mistral Cohere DeepSeek Qwen model news 2026"
20. "AI model benchmark LMSYS Chatbot Arena MMLU HumanEval leaderboard 2026"
21. "arxiv AI paper multimodal reasoning small language model notable week 2026"
22. "Med-Gemini AlphaFold medical AI agentic multi-agent 2026"

LAYER 4 — APPLICATIONS:
23. "Claude ChatGPT Gemini Copilot Perplexity product update feature this week 2026"
24. "AI real estate property valuation AVM PropTech construction smart building 2026"
25. "AI banking credit scoring algorithmic trading fraud detection robo-advisor 2026"
26. "AI airport logistics autonomous vehicle drone supply chain 2026"
27. "AI education tutoring Khan Academy Duolingo EdTech 2026"
28. "AI healthcare medical imaging drug discovery clinical AI FDA approval 2026"
29. "AI customer service enterprise Salesforce Agentforce ServiceNow SAP 2026"
30. "AI cybersecurity legal tech HR tech GitHub Copilot Cursor 2026"
31. "Vietnam AI startup technology application 2026"

══════════════════════════════════════════════════════════════════════════════════
SAU KHI HOÀN THÀNH TẤT CẢ TÌM KIẾM, viết báo cáo theo đúng mẫu sau.
Giữ nguyên các ký tự phân cách ━ ─ ⚡ ▶ và cấu trúc header.
══════════════════════════════════════════════════════════════════════════════════

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AI WEEKLY | Tuần {week_num} · {date_str}
Tổng hợp bởi Claude · Khung phân tích: Johnson Wang 4-Layer AI Stack
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ 3 SIGNAL QUAN TRỌNG NHẤT TUẦN NÀY
• [Signal 1: mô tả diễn biến cụ thể → tại sao quan trọng chiến lược → hàm ý 6-12 tháng tới. 2 câu súc tích.]
• [Signal 2: tương tự — 2 câu súc tích.]
• [Signal 3: tương tự — 2 câu súc tích.]

─── LAYER 1 · HARDWARE & INFRASTRUCTURE ────────────────────────────────────

[I.A] CHIP & BÁN DẪN
• NVIDIA: [tin tuần này về GPU mới / roadmap / doanh số / thị phần — tên model + số liệu cụ thể]
• Đối thủ alternatives: [AMD MI300X+ / Intel Gaudi / Google TPU / AWS Trainium — update đáng chú ý]
• Custom Silicon: [Apple / Meta MTIA / Tesla Dojo / Qualcomm — ai đang làm được gì?]
• Startup chip: [Cerebras / Groq / SambaNova / Tenstorrent — news & funding tuần này]
• Semiconductor geopolitics: [export controls / TSMC / Samsung / Intel Foundry — diễn biến mới]

[I.B] DATA CENTER & POWER INFRASTRUCTURE
• Hyperscaler capex: [Microsoft/AWS/Google/Meta spend bao nhiêu, build ở đâu — số liệu tỷ USD]
• Power crisis: [AI data center tiêu thụ điện — nuclear/renewable solutions mới nhất]
• Cooling tech: [liquid cooling / immersion cooling — breakthrough tuần này nếu có]

[I.C] KHÔNG GIAN & VIỄN THÔNG
• SpaceX Starlink: [capacity mới / orbital shell / enterprise AI use case — tin tuần này]
• Rocket launches: [liên quan satellite internet / earth observation — đáng chú ý]
• 6G & undersea cables: [dự án mới ảnh hưởng AI latency — nếu có]

▶ INSIGHT LAYER 1: [1-2 câu phân tích: điều gì ở hardware/infra layer đang tạo ra \
bottleneck hoặc breakthrough quan trọng nhất cho AI toàn cầu tuần này?]

─── LAYER 2 · DATA & CLOUD ──────────────────────────────────────────────────

[II.A] HYPERSCALER MOVEMENT
• Microsoft Azure AI: [sản phẩm mới / partnership / pricing — tin tuần này + số liệu]
• AWS (Bedrock/SageMaker): [launch mới / enterprise deal đáng chú ý]
• Google Cloud (Vertex AI): [update / Workspace AI integration mới]
• Meta (infrastructure/open-source): [Llama ecosystem / PyTorch / data tools]
• Nhận định: [hyperscaler nào đang winning enterprise AI race tuần này và vì sao?]

[II.B] CÔNG CỤ XỬ LÝ & QUẢN LÝ DỮ LIỆU
• Data pipeline: [Databricks / Snowflake / dbt — tính năng mới đáng chú ý]
• Vector DB & RAG: [Pinecone / Weaviate / Chroma / pgvector — update tuần này]
• Synthetic data & governance: [tools / startups / use case mới nhất]
• Open datasets: [dataset mới release từ Hugging Face / academic — nếu có]

[II.C] EDGE AI & ON-DEVICE
• [Apple Intelligence / Qualcomm NPU / MediaTek APU — on-device AI news tuần này]
• [Federated learning / privacy-preserving ML — breakthrough nếu có]

▶ INSIGHT LAYER 2: [1-2 câu: Data layer đang có bottleneck hay breakthrough gì quan trọng? \
Hyperscaler nào đang tạo ra data moat đáng kể?]

─── LAYER 3 · MODELS & RESEARCH ─────────────────────────────────────────────

[III.A] FRONTIER MODELS — RELEASE & BENCHMARK
• Anthropic (Claude): [model mới / tính năng / safety research / pricing — tuần này]
• OpenAI (GPT/o-series/Sora): [release mới / API update / benchmark so sánh]
• Google DeepMind (Gemini/Gemma/Veo): [update đáng chú ý]
• Meta (Llama): [open-source release mới / fine-tuning ecosystem]
• Others (xAI Grok / Mistral / Cohere / DeepSeek / Qwen): [news tuần này]
• Benchmark snapshot: [LMSYS Chatbot Arena / MMLU / HumanEval — ai đang dẫn đầu?]

[III.B] KIẾN TRÚC & PHƯƠNG PHÁP HUẤN LUYỆN
(Tối đa 3 ArXiv paper đáng chú ý tuần này — mỗi paper: tên → ý tưởng chính → ý nghĩa thực tiễn)
• Paper 1: [tên paper] — [ý tưởng chính 1 câu] → Ý nghĩa: [1 câu tác động thực tế]
• Paper 2: [tương tự]
• Paper 3: [tương tự — nếu có]
• Multimodal & Reasoning: [breakthrough mới nhất trong text+image+audio+video+action]
• Small Language Models: [phi-4 / Gemma 3 / Llama 3.x — news mới]

[III.C] SPECIALIZED & DOMAIN MODELS
• Y tế/Khoa học: [Med-Gemini / AlphaFold / bioinformatics AI — update mới nhất]
• Agentic AI: [tool use / multi-agent systems — breakthrough trong tuần]
• Open-source vs closed-source: [tương quan lực lượng đang thay đổi như thế nào?]

▶ INSIGHT LAYER 3: [1-2 câu: Model/paper nào đang thực sự dịch chuyển state-of-the-art? \
Race giữa các lab đang đến giai đoạn nào?]

─── LAYER 4 · APPLICATIONS ──────────────────────────────────────────────────

[IV.A] SẢN PHẨM AI FLAGSHIP
• Claude: [tính năng mới / pricing / API update / integrations — tuần này]
• ChatGPT/GPT-4o: [update / new features / plugin mới]
• Gemini: [tính năng mới trên Workspace / mobile / API]
• Copilot: [tích hợp mới vào Office 365 / Azure / GitHub]
• Nổi bật: [Perplexity / Cursor / Midjourney / Runway / ElevenLabs / HeyGen — news]
• Startup viral tuần này: [tên + lý do nổi bật]

[IV.B] BẤT ĐỘNG SẢN
• AI định giá (AVM): [công cụ/startup mới / accuracy cải thiện — số liệu]
• AI tìm kiếm & môi giới: [Zillow AI / PropertyGuru / Proptech VN — update]
• Construction tech: [AI thiết kế / quản lý dự án / quantity surveying]
• Smart building: [AI vận hành tòa nhà / tiết kiệm năng lượng — case study cụ thể]
• Case study VN: [AI đang được developers/agencies VN áp dụng như thế nào?]

[IV.C] NGÂN HÀNG & TÀI CHÍNH
• AI credit scoring & underwriting: [model mới / accuracy / bias concerns — số liệu]
• Algorithmic trading & quant: [AI strategy mới / hedge fund moves tuần này]
• Fraud detection: [breakthrough mới / effectiveness metrics]
• AI financial advisor: [Betterment / Wealthfront / VN fintechs — update]
• LLM trong phân tích tài chính: [earnings call analysis / báo cáo tài chính — use case mới]

[IV.D] SÂN BAY & LOGISTICS
• Airport AI: [biometric boarding / baggage tracking / ATC AI / predictive maintenance]
• Autonomous & drones: [delivery drone / AV deployment — news tuần này]
• Supply chain AI: [disruption detection / demand forecasting / warehouse robotics]
• VN context: [Nội Bài / Tân Sơn Nhất smart airport; VN logistics tech — update]

[IV.E] GIÁO DỤC
• AI tutoring: [Khan Academy Khanmigo / Duolingo AI / Coursera AI — update]
• Chính sách AI đại học: [trường top mới nhất — quy định / tools cho giảng viên]
• Assessment AI: [vấn đề đạo đức / giải pháp mới]
• VN EdTech AI: [startup/ứng dụng đáng chú ý]

[IV.F] Y TẾ
• AI diagnostic imaging: [FDA approval mới / accuracy benchmark / deployment scale]
• Drug discovery: [AlphaFold applications / generative chemistry / trial results]
• Clinical AI: [ambient documentation Nuance DAX/Suki / clinical decision support]
• Wearable & remote monitoring: [Apple Health / Fitbit — AI features mới]
• VN HealthTech: [ứng dụng/startup đáng chú ý]

[IV.G] DỊCH VỤ & CÔNG NGHỆ
• Customer service AI: [conversational AI platform mới / deflection rate improvements]
• Enterprise AI agents: [Salesforce Agentforce / ServiceNow / SAP AI — update]
• Legal & HR tech AI: [Harvey AI / Clio / LexisNexis / recruiting AI — news]
• Software dev AI: [GitHub Copilot / Cursor / Devin / AI code review — update tuần này]
• Cybersecurity AI: [threat detection / AI-powered SOC / red teaming — news]

▶ INSIGHT LAYER 4: [1-2 câu: Ứng dụng nào đang tạo ROI thực sự? \
Industry nào đang bị disrupted mạnh nhất bởi AI tuần này?]

─── LAYER 5 · POV & SCOREBOARD ──────────────────────────────────────────────

[V.A] 3 SIGNAL QUAN TRỌNG NHẤT — PHÂN TÍCH SÂU
(3 diễn biến có ý nghĩa chiến lược dài hạn — không phải 3 tin hot nhất)

Signal 1: [Tên signal]
→ Diễn biến: [mô tả cụ thể]
→ Tại sao quan trọng: [phân tích 2-3 câu]
→ Hàm ý 6-12 tháng tới: [dự báo có thể hành động]

Signal 2: [Tên signal]
→ Diễn biến: [...]
→ Tại sao quan trọng: [...]
→ Hàm ý 6-12 tháng tới: [...]

Signal 3: [Tên signal]
→ Diễn biến: [...]
→ Tại sao quan trọng: [...]
→ Hàm ý 6-12 tháng tới: [...]

[V.B] AI RACE SCOREBOARD — Snapshot tương quan lực lượng hiện tại
• Model capability: [ai đang dẫn đầu? khoảng cách với nhau là gì?]
• Infrastructure (compute): [ai đang có lợi thế compute lớn nhất?]
• Enterprise adoption: [ai đang winning B2B và bằng chứng nào?]
• Consumer: [ai đang dominate end-user và tại sao?]
• Open-source ecosystem: [ai đang winning developer mindshare?]

[V.C] WHAT TO WATCH NEXT WEEK
• [Sự kiện/phát triển 1: tên cụ thể + ngày + lý do đáng theo dõi]
• [Sự kiện/phát triển 2: tương tự]
• [Sự kiện/phát triển 3 nếu có: tương tự]

─── NGUỒN THAM KHẢO TUẦN NÀY ────────────────────────────────────────────────
[Liệt kê tất cả nguồn đã sử dụng theo format: Tên nguồn · URL (nếu có) · Ngày đăng]
"""


def build_prompt(date_str: str, week_num: int, date_from: str, date_to: str) -> str:
    """Return the fully-rendered AI Weekly prompt."""
    return _PROMPT_TEMPLATE.format(
        date_str=date_str,
        week_num=week_num,
        date_from=date_from,
        date_to=date_to,
    )
