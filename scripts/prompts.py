"""Session prompts and configuration for the Vietnam RE daily report."""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Session registry — keyed by Python weekday (0=Mon … 3=Thu)
# ---------------------------------------------------------------------------
SESSIONS: dict[int, dict] = {
    0: {
        "id": "A",
        "name": "RESIDENTIAL (BUILD TO SELL)",
        "thu": "Thứ 2",
        "email_prefix": "Residential",
    },
    1: {
        "id": "B",
        "name": "HOSPITALITY, ENTERTAINMENT & SERVICED APARTMENT",
        "thu": "Thứ 3",
        "email_prefix": "Hospitality",
    },
    2: {
        "id": "C",
        "name": "RETAIL & OFFICE (BUILD TO LEASE)",
        "thu": "Thứ 4",
        "email_prefix": "Retail & Office",
    },
    3: {
        "id": "D",
        "name": "INDUSTRIAL: KCN, TECHNOLOGY PARK & DATA CENTER",
        "thu": "Thứ 5",
        "email_prefix": "Industrial",
    },
}


# ---------------------------------------------------------------------------
# Shared preamble injected into every prompt
# ---------------------------------------------------------------------------
_COMMON_PREAMBLE = """\
Hôm nay là {thu_str}, {date_str} (giờ Việt Nam).

Bạn là chuyên gia chiến lược bất động sản cấp senior, kết hợp góc nhìn của nhà đầu tư, \
developer và tư vấn chiến lược. Tiêu chuẩn phân tích: McKinsey/BCG — số liệu cụ thể, \
phân tích có chiều sâu, insight có tính hành động, KHÔNG viết chung chung.

TIÊU CHUẨN ĐẦU RA:
• Mỗi bullet PHẢI có số liệu hoặc ví dụ cụ thể.
• Nếu không có dữ liệu 7 ngày qua, ghi: "Chưa có cập nhật mới — số liệu gần nhất: [ngày] từ [nguồn]."
• KHÔNG bịa số liệu.
• Tổng dài báo cáo: 1.500–2.000 từ. Mỗi phần 300–500 từ.
• Ngôn ngữ: Tiếng Việt. Văn phong chuyên nghiệp, súc tích.

NGUỒN ƯU TIÊN (tìm kiếm từ 7 ngày qua trước):
Savills, CBRE, JLL, Cushman & Wakefield, Knight Frank, McKinsey GI, BCG, Bain, \
Mordor Intelligence, Bloomberg, Reuters, VnExpress, Cafef, Reatimes, Tạp chí BĐS VN, \
Bộ Xây dựng.\
"""

_COMMON_FOOTER = """\

─── NGUỒN THAM KHẢO HÔM NAY ───────────────────────────────────────────────
[Liệt kê tất cả nguồn đã sử dụng: Tên nguồn · URL (nếu có) · Ngày đăng]
"""


# ---------------------------------------------------------------------------
# SESSION A — RESIDENTIAL
# ---------------------------------------------------------------------------
_PROMPT_A = (
    _COMMON_PREAMBLE
    + """

NHIỆM VỤ: Nghiên cứu và viết báo cáo thị trường BĐS RESIDENTIAL (Build to Sell) Việt Nam.
Thị trường trọng điểm: TP.HCM, Hà Nội, Đà Nẵng, Bình Dương, Đồng Nai, Long An, Bà Rịa–Vũng Tàu.

HƯỚNG DẪN TÌM KIẾM — tìm lần lượt các cụm từ sau:
1. "thị trường căn hộ chung cư tuần này {date_str}" HOẶC "bất động sản nhà ở tháng 5 2025"
2. "Savills CBRE JLL Vietnam residential market Q1 2025"
3. "giá căn hộ TP.HCM Hà Nội {date_str}"
4. "tồn kho căn hộ absorption rate Vietnam 2025"
5. "lãi suất vay mua nhà ngân hàng Việt Nam mới nhất 2025"
6. "dự án bất động sản mới ra mắt TP.HCM 2025"
7. "Luật Đất đai 2024 nghị định thông tư mới nhất"
8. "PropTech AI định giá bất động sản Việt Nam 2025"
9. "Build-to-Rent BTR affordable housing Asia 2025"
10. "McKinsey BCG housing market report 2025"

SAU KHI TÌM KIẾM, viết báo cáo theo đúng mẫu sau (giữ nguyên ký tự ━ ─ ⚡ ★ ✦):

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RESIDENTIAL DEEP DIVE | {thu_str}, {date_str}
Tổng hợp bởi Claude · Nguồn: Savills / CBRE / JLL / [nguồn chính hôm nay]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ TÓM TẮT ĐIỀU HÀNH (đọc trong 60 giây)
• [Số liệu/tin quan trọng nhất hôm nay — phải có con số cụ thể]
• [Insight chiến lược nổi bật nhất — phải actionable]
• [Điều cần theo dõi trong tuần tới]

─── I. CHỈ SỐ THỊ TRƯỜNG ──────────────────────────────────────────────────

Phân tích theo 4 phân khúc:

**Affordable (<2 tỷ VNĐ):**
- Khối lượng giao dịch: [X căn] ([+/-X% WoW] | [+/-X% YoY]) — Nguyên nhân: [giải thích]
- Giá sơ cấp: [X triệu/m²] | Thứ cấp: [X triệu/m²] | Biến động: [+/-X%]
  → Thị trường/dự án kéo giá: [tên cụ thể]
- Absorption rate: [X%] | Tồn kho: [X căn] ([Y tháng tồn])
- Lãi suất vay: [X%/năm] (nguồn: [tên ngân hàng/NHNN])

**Mid-end (2–5 tỷ VNĐ):**
[Tương tự format trên, với số liệu riêng biệt]

**High-end (5–15 tỷ VNĐ):**
[Tương tự format trên, với số liệu riêng biệt]

**Luxury (>15 tỷ VNĐ):**
[Tương tự format trên, với số liệu riêng biệt]

📌 Highlight: [Phân khúc nào đang outperform/underperform và tại sao — phân tích 3–4 câu \
có số liệu]

─── II. PLAYER & DỰ ÁN NỔI BẬT ────────────────────────────────────────────

[Liệt kê 3–5 dự án/tin, mỗi tin theo format:]

**[Tên dự án]**
- Chủ đầu tư: [tên] | Vị trí: [địa chỉ cụ thể]
- Quy mô: [số căn/tổng GFA] | Giá: [X triệu–Y triệu/m²]
- Tỷ lệ bán/hấp thụ: [X%] | Tổng giá trị: [X tỷ VNĐ]
- Điểm đặc biệt: [lý do tin này đáng chú ý — tỷ lệ bán bất thường, M&A, chủ đầu tư mới, \
sản phẩm độc đáo v.v.]

─── III. PHÁP LÝ & CHÍNH SÁCH ─────────────────────────────────────────────

[Mỗi mục: Nêu chính sách (số hiệu, ngày) → Tác động thực tế → Ai được lợi/bất lợi]

• **Luật Đất đai 2024 / Luật Nhà ở 2023 / Luật KDBĐS 2023:**
  [Nghị định/thông tư mới nhất — số hiệu + ngày ban hành + nội dung chính]
  → Tác động: [buyer / developer / investor được lợi/bất lợi như thế nào?]

• **Chính sách tín dụng/thuế/quy hoạch tuần này:**
  [Cụ thể hóa từng chính sách]
  → Tác động: [...]

• **Nhận định tổng hợp:** [Chính sách tháng này đang tạo tailwind hay headwind \
cho thị trường? Vì sao?]

─── IV. XU HƯỚNG QUỐC TẾ ──────────────────────────────────────────────────

• **PropTech:** [AI định giá / virtual staging / digital mortgage / tokenization BĐS — \
ví dụ công ty cụ thể + số liệu tác động]
• **Mô hình toàn cầu:** [BTR / affordable housing / mixed-income development — \
case study mới nhất từ Mỹ/châu Á/châu Âu]
• **Báo cáo McKinsey/BCG/Bain (nếu có):** [Tên báo cáo + insight chính liên quan \
housing]
• **Liên hệ thị trường VN:** [Xu hướng quốc tế nào đang/sẽ ảnh hưởng đến VN? \
Thời gian dự kiến tác động?]

─── V. POINT OF VIEW CHIẾN LƯỢC ───────────────────────────────────────────

**A. XU HƯỚNG DỊCH CHUYỂN NGÀNH (3–4 điểm)**
[Mỗi điểm: Tên shift + Bằng chứng cụ thể + Dự báo 12–24 tháng]

1. [Shift cơ cấu cầu — demographics/lifestyle]
   Bằng chứng: [...] | Dự báo: [...]

2. [Shift nguồn cung — loại hình mới nổi]
   Bằng chứng: [...] | Dự báo: [...]

3. [Shift tài chính — cấu trúc deal/vốn]
   Bằng chứng: [...] | Dự báo: [...]

4. [Shift địa lý — thị trường mới nổi vs bão hòa]
   Bằng chứng: [...] | Dự báo: [...]

**B. WHERE TO PLAY — Nên cạnh tranh ở đâu?**

(1) Phân khúc giá có structural demand gap: [tên phân khúc + lý do + số liệu]
(2) Địa lý underserved hoặc momentum tốt: [tên địa phương + evidence cụ thể]
(3) Loại hình sản phẩm đang capture emerging demand: [tên + ví dụ dự án cụ thể]

→ 2–3 "bet" cho developer/investor trong 18 tháng tới:
  ★ Bet 1: [Tên + lý do + upside kỳ vọng]
  ★ Bet 2: [...]
  ★ Bet 3: [...]

**C. HOW TO WIN — Chiến lược cạnh tranh**

(1) Differentiation của leading developers: [ví dụ Vingroup/Novaland/Masterise/khác \
+ số liệu]
(2) Ai đang winning và vì sao: [tên developer + evidence]
(3) Moat bền vững trong phân khúc này: [2–3 yếu tố với ví dụ cụ thể]

→ 2–3 năng lực cốt lõi cần xây dựng:
  ✦ [Năng lực 1 — mô tả cụ thể]
  ✦ [Năng lực 2]
  ✦ [Năng lực 3]
"""
    + _COMMON_FOOTER
)


# ---------------------------------------------------------------------------
# SESSION B — HOSPITALITY, ENTERTAINMENT & SERVICED APARTMENT
# ---------------------------------------------------------------------------
_PROMPT_B = (
    _COMMON_PREAMBLE
    + """

NHIỆM VỤ: Nghiên cứu và viết báo cáo thị trường HOSPITALITY, ENTERTAINMENT & \
SERVICED APARTMENT Việt Nam.
Thị trường trọng điểm: TP.HCM, Hà Nội, Đà Nẵng, Phú Quốc, Nha Trang, Hội An, \
Đà Lạt, Phan Thiết.
Phân loại: Hotel branded / Hotel unbranded / Resort / Integrated Resort / \
Serviced Apartment / Condotel / Entertainment venue.

HƯỚNG DẪN TÌM KIẾM:
1. "Vietnam hotel occupancy ADR RevPAR {date_str} 2025"
2. "Savills CBRE JLL Vietnam hospitality market Q1 2025"
3. "Vietnam tourism arrivals statistics 2025 latest"
4. "serviced apartment Ho Chi Minh Hanoi occupancy rent 2025"
5. "condotel legal status Vietnam 2025 update"
6. "Quyết định 26/2025 TPHCM căn hộ dịch vụ"
7. "integrated resort theme park Vietnam entertainment 2025"
8. "Airbnb short-term rental regulation Vietnam 2025"
9. "AI revenue management hospitality IHG Marriott 2025"
10. "sustainability green hotel certification Vietnam 2025"
11. "Vietnam international tourist arrivals 2025"

SAU KHI TÌM KIẾM, viết báo cáo theo đúng mẫu sau:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HOSPITALITY DEEP DIVE | {thu_str}, {date_str}
Tổng hợp bởi Claude · Nguồn: Savills / CBRE / JLL / [nguồn chính hôm nay]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ TÓM TẮT ĐIỀU HÀNH (đọc trong 60 giây)
• [Số liệu/tin quan trọng nhất hôm nay — phải có con số cụ thể]
• [Insight chiến lược nổi bật nhất — phải actionable]
• [Điều cần theo dõi trong tuần tới]

─── I. CHỈ SỐ THỊ TRƯỜNG ──────────────────────────────────────────────────

**HOTEL & RESORT:**

Theo thị trường & phân khúc (Luxury / Upscale / Midscale):

| Thị trường | Phân khúc | Occupancy | ADR (USD) | RevPAR | YoY |
|------------|-----------|-----------|-----------|--------|-----|
| TP.HCM     | Luxury    | X%        | $X        | $X     | +X% |
| TP.HCM     | Upscale   | X%        | $X        | $X     | +X% |
| Hà Nội     | Luxury    | X%        | $X        | $X     | +X% |
| Đà Nẵng    | Upscale   | X%        | $X        | $X     | +X% |
| Phú Quốc   | Luxury    | X%        | $X        | $X     | +X% |
[Thêm các thị trường/phân khúc khác nếu có dữ liệu]

• ADR branded vs unbranded: chênh lệch [X%] — đang thu hẹp/mở rộng vì [lý do]
• Pipeline 12 tháng: [X phòng] sắp vào thị trường — rủi ro oversupply tại [địa điểm cụ thể]

**SERVICED APARTMENT:**
• Occupancy: [X%] TP.HCM | [X%] Hà Nội — biến động [+/-X%] YoY
• Giá thuê trung bình:
  - Grade A: $[X]/tháng/căn
  - Grade B: $[X]/tháng/căn
• Lease-up pace dự án mới: [X căn/tháng]
• Cơ cấu khách: Expat corporate [X%] | Expat family [X%] | Digital nomad [X%] | \
Short-term [X%]

**ENTERTAINMENT:**
• [Tin tức integrated resort / theme park / F&B destination mới với số liệu cụ thể]
• Footfall/traffic: [số liệu nếu có, ghi nguồn]

─── II. PLAYER & DỰ ÁN NỔI BẬT ────────────────────────────────────────────

[3–5 tin theo format:]

**[Tên dự án/thương vụ]**
- Loại: [Hotel / Resort / Serviced Apartment / Entertainment / M&A]
- Chủ đầu tư/Operator: [tên] | Vị trí: [địa chỉ cụ thể]
- Quy mô: [số phòng/GFA] | Phân khúc: [Luxury/Upscale/Midscale]
- Tình trạng: [Khai trương / Đang triển khai / Pre-leasing / Ký kết HĐ quản lý]
- Điểm đặc biệt: [lý do đáng chú ý — operator mới, concept độc đáo, M&A, rebranding]

─── III. PHÁP LÝ & CHÍNH SÁCH ─────────────────────────────────────────────

• **Quyết định 26/2025 TPHCM (căn hộ dịch vụ):**
  [Nội dung triển khai thực tế → tác động đến operators/investors]

• **Condotel — tình trạng pháp lý hiện tại:**
  [Nghị định/thông tư mới nhất về pháp lý condotel → tác động đến thị trường]

• **Kinh doanh lưu trú ngắn hạn (Airbnb/OTA):**
  [Quy định mới + thực thi thực tế → tác động đến operators]

• **Casino/Entertainment phức hợp — điều kiện cấp phép:**
  [Cập nhật mới nhất → ai được lợi?]

• **Tác động tổng hợp:** [Nhận định về môi trường pháp lý ngành hospitality \
hiện tại — thuận lợi hay khó khăn?]

─── IV. XU HƯỚNG QUỐC TẾ ──────────────────────────────────────────────────

• **AI trong revenue management:** [Ví dụ cụ thể từ IHG ONE / Marriott Bonvoy AI \
/ Hilton — kết quả đo lường được]
• **Sustainability:** [Net-zero hospitality — ai đang dẫn đầu? LEED/BREEAM/Green \
Key — số liệu chứng nhận]
• **Mô hình mới:** [Co-living / hybrid stay / bleisure / wellness resort — \
case study thực tế 2025]
• **Recovery du lịch toàn cầu:** [Số liệu cross-border travel → VN hưởng lợi \
như thế nào?]

─── V. POINT OF VIEW CHIẾN LƯỢC ───────────────────────────────────────────

**A. XU HƯỚNG DỊCH CHUYỂN NGÀNH (3–4 điểm)**
[Shift về traveler profile / loại hình lưu trú / vai trò entertainment / \
cơ cấu doanh thu]

1. [Shift về traveler profile (Gen Z vs Millennial vs HNWIs)]
   Bằng chứng: [...] | Dự báo: [...]

2. [Shift loại hình lưu trú ưa chuộng]
   Bằng chứng: [...] | Dự báo: [...]

3. [Shift vai trò entertainment trong hospitality mix]
   Bằng chứng: [...] | Dự báo: [...]

4. [Shift cơ cấu doanh thu (F&B/MICE/ancillary vs room revenue)]
   Bằng chứng: [...] | Dự báo: [...]

**B. WHERE TO PLAY**

(1) Destination nào ở VN đang có gap cầu vs cung quality: [tên + evidence]
(2) Phân khúc có cơ hội tốt nhất 2025–2027: [budget/lifestyle/luxury/wellness/\
integrated resort + lý do]
(3) Loại SA được corporate demand absorb tốt nhất: [loại + số liệu]

→ 2–3 "bet" cho investor/operator trong 18 tháng tới:
  ★ Bet 1: [...]
  ★ Bet 2: [...]
  ★ Bet 3: [...]

**C. HOW TO WIN**

(1) Branded vs independent — khi nào chọn operator quốc tế, khi nào tự vận hành: \
[tiêu chí + ví dụ]
(2) Differentiation thực tế từ operators đang outperform tại VN và ĐNA: [tên + \
evidence]
(3) Moat thực sự trong hospitality: [location / brand / loyalty ecosystem / \
operational excellence — phân tích có số liệu]

→ 2–3 năng lực cốt lõi cần xây dựng:
  ✦ [Năng lực 1]
  ✦ [Năng lực 2]
  ✦ [Năng lực 3]
"""
    + _COMMON_FOOTER
)


# ---------------------------------------------------------------------------
# SESSION C — RETAIL & OFFICE
# ---------------------------------------------------------------------------
_PROMPT_C = (
    _COMMON_PREAMBLE
    + """

NHIỆM VỤ: Nghiên cứu và viết báo cáo thị trường RETAIL & OFFICE (Build to Lease) VN.
Thị trường trọng điểm: TP.HCM (CBD Q1/Q3/Thủ Thiêm; Non-CBD Phú Mỹ Hưng/Bình Thạnh) \
| Hà Nội (CBD Hoàn Kiếm/Ba Đình/Tây Hồ Tây; Non-CBD Cầu Giấy/Gia Lâm).

HƯỚNG DẪN TÌM KIẾM:
1. "Vietnam Grade A office occupancy rent {date_str} 2025 CBRE JLL Savills"
2. "office market Ho Chi Minh Hanoi Q1 2025 net absorption"
3. "Vietnam retail mall occupancy rent 2025"
4. "co-working flexible office Vietnam expansion 2025"
5. "Vietnam CBD office sublease rate 2025"
6. "retail tenant mix F&B fashion entertainment mall Vietnam"
7. "hybrid work office demand Vietnam 2025 badge data"
8. "green building LEED EDGE Vietnam office 2025"
9. "PCCC quy định phòng cháy chữa cháy tòa nhà 2025"
10. "experiential retail concept Asia case study 2025"
11. "CBRE JLL Savills office retail outlook Vietnam Q1 2025 report"

SAU KHI TÌM KIẾM, viết báo cáo theo đúng mẫu sau:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RETAIL & OFFICE DEEP DIVE | {thu_str}, {date_str}
Tổng hợp bởi Claude · Nguồn: Savills / CBRE / JLL / [nguồn chính hôm nay]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ TÓM TẮT ĐIỀU HÀNH (đọc trong 60 giây)
• [Số liệu/tin quan trọng nhất hôm nay — phải có con số cụ thể]
• [Insight chiến lược nổi bật nhất — phải actionable]
• [Điều cần theo dõi trong tuần tới]

─── I. CHỈ SỐ THỊ TRƯỜNG ──────────────────────────────────────────────────

**OFFICE — TP.HCM:**

| Grade | Sub-market | Occupancy | Net Abs (m²) | Rent (USD/m²/th) | QoQ | YoY |
|-------|------------|-----------|--------------|------------------|-----|-----|
| A     | CBD        | X%        | X,XXX        | $X               | +X% | +X% |
| A     | Non-CBD    | X%        | X,XXX        | $X               | +X% | +X% |
| B     | CBD        | X%        | X,XXX        | $X               | +X% | +X% |
| B     | Non-CBD    | X%        | X,XXX        | $X               | +X% | +X% |

**OFFICE — Hà Nội:**
[Tương tự format trên]

• Demand by sector: Tech/Fintech [X%] | Financial Services [X%] | FMCG [X%] | \
Logistics [X%] | Consulting [X%]
• Tỷ lệ sublease (chỉ số sức khỏe): [X%] — đang tăng/giảm vì [lý do]
• Flight-to-quality: [X,XXX m²] chuyển từ Grade B sang Grade A trong quý — \
tác động đến từng grade

**RETAIL:**

| Format | Thị trường | Occupancy | Giá thuê prime | Rental reversion | Footfall |
|--------|------------|-----------|----------------|------------------|---------|
| Regional Mall | TP.HCM | X% | X.XXX.XXX đ/m²/th | +X% | X triệu lượt/th |
| Community Mall | TP.HCM | X% | X.XXX.XXX đ/m²/th | +X% | — |
| High Street | Hà Nội | X% | X.XXX.XXX đ/m²/th | +X% | — |
[Thêm format/thị trường khác nếu có dữ liệu]

• Tenant mix điển hình top malls: F&B [X%] | Fashion [X%] | Entertainment [X%] \
| Grocery [X%] | Services [X%]
• Tenant đáng chú ý tuần này: [mới ký / rời đi / concept store mới]

─── II. PLAYER & DỰ ÁN NỔI BẬT ────────────────────────────────────────────

[3–5 tin theo format:]

**[Tên dự án/tòa nhà/thương vụ]**
- Loại: [Grade A Office / Retail Mall / Co-working / M&A / Asset Repositioning]
- Chủ đầu tư/Developer: [tên] | Vị trí: [địa chỉ + sub-market]
- Quy mô: [GFA m²] | Pre-leasing: [X% đã ký]
- Tenant anchor: [tên tenant + diện tích]
- Điểm đặc biệt: [lý do đáng chú ý — pre-leasing lớn, concept mới, M&A, anchor mới]

─── III. PHÁP LÝ & CHÍNH SÁCH ─────────────────────────────────────────────

• **Quy hoạch phân khu CBD TP.HCM & Hà Nội:**
  [Cập nhật mới nhất → ảnh hưởng đến office/retail supply pipeline]

• **Tiêu chuẩn công trình xanh (LEED/EDGE/Green Mark):**
  [Chính sách khuyến khích mới / yêu cầu bắt buộc → tác động chi phí developer]

• **Quy định PCCC mới:**
  [Yêu cầu mới → ảnh hưởng thiết kế/vận hành tòa nhà — tác động chi phí]

• **Điều kiện cấp phép bán lẻ cho nhà đầu tư nước ngoài:**
  [Quy định hiện hành + thay đổi mới nhất → cơ hội/rào cản]

• **Tác động tổng hợp:** [...]

─── IV. XU HƯỚNG QUỐC TẾ ──────────────────────────────────────────────────

• **Hybrid work & office rightsizing:** [Badge data tại thị trường lớn (NYC/London/\
Singapore) → thực tế net demand giảm X% → tác động đến VN?]
• **Experiential retail:** [Case study thành công mới nhất 2025 (Châu Á/Mỹ/EU) — \
tên concept + KPI cụ thể]
• **PropTech for office:** [Smart building / AI energy management / workplace \
analytics — ví dụ cụ thể + ROI]
• **Báo cáo CBRE/JLL/Savills Q1 2025:** [Key findings nếu đã phát hành]

─── V. POINT OF VIEW CHIẾN LƯỢC ───────────────────────────────────────────

**A. XU HƯỚNG DỊCH CHUYỂN NGÀNH (3–4 điểm)**

1. [OFFICE: Permanent shift sang hybrid — net demand thực sự giảm X% tại VN]
   Bằng chứng: [...] | Dự báo: [...]

2. [OFFICE: Flight-to-quality — Grade B mất tenant sang Grade A]
   Bằng chứng: [...] | Dự báo: [...]

3. [RETAIL: Physical retail VN chống lại e-commerce — loại hình nào immune?]
   Bằng chứng: [...] | Dự báo: [...]

4. [RETAIL/OFFICE: ESG & green building trở thành yêu cầu từ MNC tenants]
   Bằng chứng: [...] | Dự báo: [...]

**B. WHERE TO PLAY**

OFFICE:
(1) Grade/sub-market có yield tốt nhất trên risk-adjusted basis: [...]
(2) Flex/co-working vs conventional — cơ hội cho developer mới: [...]

RETAIL:
(1) Format underserved tại VN: [community mall / outlet / lifestyle center + \
lý do + evidence]
(2) Tỉnh/thành ngoài HN-HCM có retail demand chưa đáp ứng: [tên + dân số + \
income data]

→ 2–3 "bet" trong 18 tháng tới:
  ★ Bet 1: [...]
  ★ Bet 2: [...]
  ★ Bet 3: [...]

**C. HOW TO WIN**

OFFICE:
(1) Asset management excellence — maintain occupancy qua các chu kỳ: [chiến thuật \
cụ thể với ví dụ]
(2) Amenities/experience là deal-breaker với tenant tốt: [danh sách cụ thể + \
ví dụ tòa nhà thực tế]

RETAIL:
(1) Curation vs scale — quy mô tối thiểu viable: [X,XXX m² với lý do]
(2) Tenant mix tối ưu: [tỷ lệ cụ thể + evidence từ thị trường VN]

→ 2–3 năng lực cốt lõi cần xây dựng:
  ✦ [Năng lực 1]
  ✦ [Năng lực 2]
  ✦ [Năng lực 3]
"""
    + _COMMON_FOOTER
)


# ---------------------------------------------------------------------------
# SESSION D — INDUSTRIAL: KCN, TECHNOLOGY PARK & DATA CENTER
# ---------------------------------------------------------------------------
_PROMPT_D = (
    _COMMON_PREAMBLE
    + """

NHIỆM VỤ: Nghiên cứu và viết báo cáo thị trường INDUSTRIAL — KCN, Technology Park \
& Data Center Việt Nam.
Thị trường trọng điểm:
• Vùng ĐNB: Bình Dương, Đồng Nai, Long An, Bà Rịa–Vũng Tàu
• Vùng phía Bắc: Hải Phòng, Bắc Ninh, Bắc Giang, Hà Nam, Hưng Yên
• Vùng miền Trung: Đà Nẵng, Quảng Nam

HƯỚNG DẪN TÌM KIẾM:
1. "Vietnam industrial park occupancy rent FDI {date_str} 2025"
2. "Savills CBRE JLL Vietnam industrial market Q1 2025"
3. "FDI Vietnam manufacturing registration 2025 latest"
4. "Vietnam KCN ready-built factory rent Binh Duong Dong Nai Bac Ninh"
5. "Vietnam data center capacity expansion 2025 Viettel CMC Equinix"
6. "technology park semiconductor Vietnam 2025"
7. "China+1 supply chain Vietnam manufacturing FDI 2025"
8. "Vietnam vs Thailand Indonesia Malaysia industrial park cost comparison 2025"
9. "AI data center demand Vietnam hyperscaler AWS Azure Google 2025"
10. "global minimum tax Vietnam FDI impact 2025"
11. "green industrial park eco-industrial Vietnam ESG MNC tenant 2025"
12. "McKinsey future of Asia manufacturing report 2025"
13. "Vietnam semiconductor packaging testing assembly FDI 2025"

SAU KHI TÌM KIẾM, viết báo cáo theo đúng mẫu sau:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INDUSTRIAL DEEP DIVE | {thu_str}, {date_str}
Tổng hợp bởi Claude · Nguồn: Savills / CBRE / JLL / [nguồn chính hôm nay]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ TÓM TẮT ĐIỀU HÀNH (đọc trong 60 giây)
• [Số liệu/tin quan trọng nhất hôm nay — phải có con số cụ thể]
• [Insight chiến lược nổi bật nhất — phải actionable]
• [Điều cần theo dõi trong tuần tới]

─── I. CHỈ SỐ THỊ TRƯỜNG ──────────────────────────────────────────────────

**KCN TRUYỀN THỐNG:**

| Tỉnh/Vùng | Occupancy | Giá đất (USD/m²/50 năm) | RBF (USD/m²/th) | FDI mới (tr USD) |
|-----------|-----------|--------------------------|-----------------|------------------|
| Bình Dương | X% | $X–$X | $X | $X |
| Đồng Nai   | X% | $X–$X | $X | $X |
| Long An    | X% | $X–$X | $X | $X |
| BR–VT      | X% | $X–$X | $X | $X |
| Bắc Ninh   | X% | $X–$X | $X | $X |
| Bắc Giang  | X% | $X–$X | $X | $X |
| Hải Phòng  | X% | $X–$X | $X | $X |
[Thêm tỉnh nếu có dữ liệu]

• FDI tuần này: [X triệu USD mới đăng ký] — Top 5 quốc gia: [danh sách] — \
Top ngành: [danh sách]
• Pipeline KCN mới: [X ha được phê duyệt/triển khai tại tỉnh nào]
• So sánh chi phí cạnh tranh:

| Chỉ số | Việt Nam | Thái Lan | Indonesia | Malaysia | Ấn Độ |
|--------|----------|----------|-----------|----------|-------|
| Giá đất KCN (USD/m²) | $X | $X | $X | $X | $X |
| Lương tối thiểu (USD/th) | $X | $X | $X | $X | $X |
| Chi phí điện (USD/kWh) | $X | $X | $X | $X | $X |

**TECHNOLOGY PARK / KCNC:**
• Occupancy: [X%] | Giá thuê: [X USD/m²/tháng]
• Tenant mix: R&D [X%] | Semiconductor [X%] | Electronics [X%] | Software [X%] \
| Cleantech [X%]
• Dự án/tenant nổi bật: [chip / EV / high-tech manufacturing — tên + quy mô]

**DATA CENTER:**
• Công suất đang hoạt động: [X MW] | Pipeline: [X MW]
• Breakdown: Tier III [X MW] | Tier IV [X MW]
• Giá colocation: [X USD/kW/tháng] | PUE trung bình: [X] | Utilization: [X%]
• Major players: Viettel IDC [X MW] | CMC [X MW] | VNG [X MW] | \
Equinix [announced/X MW] | NTT [X MW]
• Hyperscaler expansion: [Microsoft Azure / AWS / Google Cloud tại VN — tin mới nhất]

─── II. PLAYER & DỰ ÁN NỔI BẬT ────────────────────────────────────────────

[3–5 tin theo format:]

**[Tên KCN/dự án/thương vụ]**
- Loại: [KCN mới / FDI lớn / Data Center / Tech Park / M&A]
- Nhà đầu tư/Developer: [tên] | Vị trí: [tỉnh/địa điểm cụ thể]
- Quy mô: [X ha / X MW / X tỷ USD vốn đầu tư]
- Ngành: [semiconductor / EV / electronics / logistics / data center]
- Tình trạng: [Đã phê duyệt / Đang triển khai / FDI mới đăng ký]
- Điểm đặc biệt: [lý do đáng chú ý — FDI >100 triệu USD, high-tech, M&A, \
player mới gia nhập]

─── III. PHÁP LÝ & CHÍNH SÁCH ─────────────────────────────────────────────

• **Quy hoạch KCN quốc gia đến 2030:**
  [Tiến độ phê duyệt KCN mới — tỉnh nào, diện tích bao nhiêu → tác động \
đến developer/investor]

• **Global Minimum Tax (Thuế tối thiểu toàn cầu 15%):**
  [Tình trạng triển khai tại VN → ảnh hưởng thu hút FDI chất lượng cao như \
thế nào? VN đang phản ứng ra sao?]

• **Data Center — tiêu chuẩn & quy định:**
  [An ninh mạng / data localization / power requirements — quy định mới nhất]

• **KCN sinh thái (Eco-Industrial Park):**
  [Tiêu chuẩn và quy định → áp lực ESG từ MNC tenants]

• **Tác động tổng hợp:** [Môi trường chính sách đang ủng hộ hay cản trở \
thu hút FDI chất lượng cao?]

─── IV. XU HƯỚNG QUỐC TẾ ──────────────────────────────────────────────────

• **China+1 & supply chain diversification:** [Số liệu mới nhất về dịch chuyển \
sản xuất — VN nhận được bao nhiêu? vs Ấn Độ/Indonesia/Mexico?]
• **Semiconductor supply chain:** [VN đang ở đâu trong chuỗi giá trị? \
Cơ hội packaging / testing / design — ví dụ cụ thể + quy mô]
• **AI infrastructure boom:** [Nhu cầu data center toàn cầu tăng X% — \
VN hưởng lợi ra sao? Hyperscaler nào đang mở rộng mạnh nhất?]
• **Green industrial park:** [Tiêu chuẩn quốc tế — ai đang dẫn đầu? \
Áp lực ESG từ MNC tenants ảnh hưởng lựa chọn địa điểm KCN]
• **Báo cáo McKinsey "Future of Asia Manufacturing" / BCG industrial RE:** \
[Key findings mới nhất]

─── V. POINT OF VIEW CHIẾN LƯỢC ───────────────────────────────────────────

**A. XU HƯỚNG DỊCH CHUYỂN NGÀNH (3–4 điểm)**

1. [Shift: Labor-cost advantage → Ecosystem advantage]
   Bằng chứng: [...] | Dự báo 2025–2030: [...]

2. [Shift: KCN thông thường vs High-tech park — phân hóa ngày càng rõ]
   Bằng chứng: [...] | Dự báo: [...]

3. [Shift: Data center từ "nice to have" → critical infrastructure]
   Bằng chứng: [...] | Dự báo: [...]

4. [Shift: ESG/net-zero trở thành yêu cầu bắt buộc từ MNC tenants]
   Bằng chứng: [...] | Dự báo: [...]

**B. WHERE TO PLAY**

(1) Tỉnh/vùng có competitive advantage thực sự theo loại hình:
  - KCN thông thường: [tỉnh + lý do — logistics / labor / utilities / ecosystem]
  - Tech Park: [tỉnh + lý do]
  - Data Center: [tỉnh + lý do — connectivity / power / proximity to cloud hubs]

(2) Phân khúc khách hàng highest-value demand: [manufacturing tier + origin \
country + industry sector + evidence]

(3) Format có demand-supply gap tốt nhất: [KCN / BTS / RBF / logistics hub / \
mixed-use industrial + evidence]

→ 2–3 "bet" trong 18 tháng tới:
  ★ Bet 1: [...]
  ★ Bet 2: [...]
  ★ Bet 3: [...]

**C. HOW TO WIN**

(1) KCN developer phải cung cấp gì ngoài đất và nhà xưởng để thắng FDI \
chất lượng cao: [danh sách cụ thể + ví dụ từ KCN đang dẫn đầu]
(2) Data center moat thực sự: [power sourcing / connectivity / PUE / tier \
certification / location — phân tích từng yếu tố với evidence]
(3) Cluster effect strategy: [Anchor tenant → supply chain → talent pool → \
supporting services — ví dụ cụ thể từ Bắc Ninh/Bình Dương/khác]

→ 2–3 năng lực cốt lõi cần xây dựng:
  ✦ [Năng lực 1]
  ✦ [Năng lực 2]
  ✦ [Năng lực 3]
"""
    + _COMMON_FOOTER
)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
_PROMPT_MAP: dict[str, str] = {
    "A": _PROMPT_A,
    "B": _PROMPT_B,
    "C": _PROMPT_C,
    "D": _PROMPT_D,
}


def build_prompt(session: dict, date_str: str) -> str:
    """Return the fully-rendered prompt for *session* on *date_str*."""
    template = _PROMPT_MAP[session["id"]]
    return template.format(
        thu_str=session["thu"],
        date_str=date_str,
    )
