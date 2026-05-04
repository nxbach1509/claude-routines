#!/usr/bin/env python3
"""
Real Estate Deep Dive — Daily Automation
Runs at 07:30 AM Vietnam time (Mon–Thu only).
Generates a market analysis report via Claude API and sends to nxbach1509@gmail.com.
"""

import anthropic
import base64
import os
import sys
from datetime import datetime, timezone, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# ── Vietnam timezone ──────────────────────────────────────────────────────────
VN_TZ = timezone(timedelta(hours=7))

# ── Day → Session mapping ─────────────────────────────────────────────────────
SESSIONS = {
    0: ("SESSION A", "RESIDENTIAL"),       # Monday
    1: ("SESSION B", "HOSPITALITY, ENTERTAINMENT & SERVICED APARTMENT"),  # Tuesday
    2: ("SESSION C", "RETAIL & OFFICE"),   # Wednesday
    3: ("SESSION D", "INDUSTRIAL (Technology Park & Data Center)"),        # Thursday
}

# ── Session-specific analysis prompts ────────────────────────────────────────
SESSION_PROMPTS = {
    0: """
Bạn là chuyên gia chiến lược bất động sản cấp senior — kết hợp góc nhìn nhà đầu tư, developer và tư vấn chiến lược (chuẩn McKinsey/BCG). Hôm nay là {date_str}. Hãy viết báo cáo SESSION A: RESIDENTIAL đầy đủ theo cấu trúc sau, bằng tiếng Việt, văn phong chuyên nghiệp, mỗi phần 300–500 từ, tổng 1.500–2.000 từ:

Thị trường trọng điểm: TP.HCM, Hà Nội, Đà Nẵng, Bình Dương, Đồng Nai, Long An, Bà Rịa–Vũng Tàu.

[I] CHỈ SỐ THỊ TRƯỜNG TUẦN NÀY — Báo cáo chi tiết theo 4 phân khúc: Affordable (<2 tỷ), Mid-end (2–5 tỷ), High-end (5–15 tỷ), Luxury (>15 tỷ). Gồm: khối lượng GD, giá sơ/thứ cấp (VND/m²), absorption rate, tồn kho, lãi suất vay mua nhà. So sánh tuần trước & YoY. Giải thích nguyên nhân.

[II] PLAYER & DỰ ÁN NỔI BẬT (3–5 tin) — Format: Tên dự án | CĐT | Vị trí | Quy mô | Giá/Tỷ lệ bán | Điểm đặc biệt. Ưu tiên: dự án mới ra mắt, tỷ lệ bán bất thường, M&A, CĐT mới.

[III] CẬP NHẬT PHÁP LÝ & CHÍNH SÁCH — Luật Đất đai 2024, Luật Nhà ở 2023, Luật KDBĐS 2023: nghị định/thông tư mới nhất. Chính sách tín dụng, thuế, quy hoạch. Phân tích tác động: có lợi/bất lợi cho ai (buyer, developer, investor)?

[IV] XU HƯỚNG & CÔNG NGHỆ QUỐC TẾ — PropTech (AI định giá, virtual staging, digital mortgage, tokenization), BTR, affordable housing models. Báo cáo McKinsey/BCG/Bain mới nhất. Liên hệ ảnh hưởng đến VN.

[V] POINT OF VIEW CHIẾN LƯỢC:
A. Xu hướng dịch chuyển ngành (3–4 điểm: bằng chứng + dự báo 12–24 tháng)
B. Where to Play: phân khúc/địa lý/loại hình sản phẩm đang có demand gap; 2–3 "bet" cụ thể 18 tháng
C. How to Win: differentiation, ai đang winning và tại sao, 2–3 năng lực cốt lõi cần xây

Cuối báo cáo: liệt kê nguồn tham khảo (tên + ngày). Nếu thiếu dữ liệu → ghi "Chưa có cập nhật mới — số liệu gần nhất: [ngày] từ [nguồn]." Không bịa số liệu.
""",
    1: """
Bạn là chuyên gia chiến lược bất động sản cấp senior. Hôm nay là {date_str}. Viết báo cáo SESSION B: HOSPITALITY, ENTERTAINMENT & SERVICED APARTMENT đầy đủ, tiếng Việt, chuẩn McKinsey/BCG, mỗi phần 300–500 từ, tổng 1.500–2.000 từ:

Thị trường: TP.HCM, HN, Đà Nẵng, Phú Quốc, Nha Trang, Hội An, Đà Lạt, Phan Thiết.

[I] CHỈ SỐ THỊ TRƯỜNG: Hotel & Resort (occupancy, ADR, RevPAR; branded vs unbranded; pipeline 12 tháng). Serviced Apartment (occupancy, giá thuê USD/tháng, cơ cấu khách). Entertainment (integrated resort, theme park, F&B destination — footfall nếu có).

[II] PLAYER & DỰ ÁN NỔI BẬT (3–5 tin): dự án khai trương mới, M&A hospitality, operator ký hợp đồng quản lý, rebranding, integrated resort.

[III] PHÁP LÝ & CHÍNH SÁCH: Quyết định 26/2025 TPHCM (căn hộ dịch vụ), condotel, Airbnb/OTA, casino/entertainment phức hợp. Tác động đến operators và investors.

[IV] XU HƯỚNG QUỐC TẾ: AI revenue management, sustainability (LEED/BREEAM), co-living, hybrid stay, bleisure, wellness resort. Recovery du lịch toàn cầu ảnh hưởng VN.

[V] POV CHIẾN LƯỢC:
A. Shifts về traveler profile, loại hình lưu trú, revenue mix
B. Where to Play: destination/phân khúc có gap tốt nhất 2025–2027; SA nào corporate demand absorb tốt nhất
C. How to Win: branded vs independent; differentiation thực tế từ operator outperform; moat trong hospitality

Liệt kê nguồn. Nếu thiếu dữ liệu → ghi rõ.
""",
    2: """
Bạn là chuyên gia chiến lược bất động sản cấp senior. Hôm nay là {date_str}. Viết báo cáo SESSION C: RETAIL & OFFICE đầy đủ, tiếng Việt, chuẩn McKinsey/BCG, mỗi phần 300–500 từ, tổng 1.500–2.000 từ:

Thị trường: TP.HCM (CBD Q1/Q3/Thủ Thiêm, Non-CBD Phú Mỹ Hưng/Bình Thạnh), HN (CBD Hoàn Kiếm/Ba Đình/Tây Hồ Tây, Non-CBD Cầu Giấy/Gia Lâm).

[I] CHỈ SỐ THỊ TRƯỜNG:
OFFICE (Grade A/B/C, CBD vs Non-CBD): occupancy, net absorption, giá thuê USD/m²/tháng + service charge. Demand by sector, sublease rate.
RETAIL (High Street/Mall/Community/Podium/Outlet): occupancy, giá thuê prime, rental reversion, footfall, tenant mix, concept mới.

[II] PLAYER & DỰ ÁN NỔI BẬT (3–5 tin): tòa office/TTTM mới, pre-leasing lớn, anchor tenant, co-working mở rộng, M&A.

[III] PHÁP LÝ: quy hoạch CBD, tiêu chuẩn xanh (LEED/EDGE), PCCC mới, điều kiện cấp phép bán lẻ nước ngoài.

[IV] XU HƯỚNG QUỐC TẾ: hybrid work + badge data, experiential retail case study, smart building/AI energy, CBRE/JLL Office Outlook Q1/2025.

[V] POV CHIẾN LƯỢC:
A. OFFICE: flight-to-quality VN, Grade B mất tenant vào A? RETAIL: physical vs e-commerce, loại hình nào immune?
B. Where to Play: Grade nào/sub-market nào yield tốt nhất? Format retail nào underserved tại VN?
C. How to Win: OFFICE asset management excellence. RETAIL: curation vs scale, tenant mix tối ưu.

Liệt kê nguồn. Nếu thiếu dữ liệu → ghi rõ.
""",
    3: """
Bạn là chuyên gia chiến lược bất động sản cấp senior. Hôm nay là {date_str}. Viết báo cáo SESSION D: INDUSTRIAL (KCN, TECHNOLOGY PARK & DATA CENTER) đầy đủ, tiếng Việt, chuẩn McKinsey/BCG, mỗi phần 300–500 từ, tổng 1.500–2.000 từ:

Thị trường: Bình Dương, Đồng Nai, Long An, BR-VT (Vùng ĐNB); HP, Bắc Ninh, Bắc Giang, Hà Nam, Hưng Yên (Phía Bắc); Đà Nẵng, Quảng Nam (Miền Trung).

[I] CHỈ SỐ THỊ TRƯỜNG:
KCN: occupancy, giá thuê đất (USD/m²/50 năm), nhà xưởng ready-built (USD/m²/tháng). FDI mới vào KCN (triệu USD), top 5 quốc gia, top ngành. Pipeline. So sánh chi phí VN vs Thái Lan/Indonesia/Malaysia/Ấn Độ.
TECHNOLOGY PARK: occupancy, giá thuê, tenant mix R&D/Semi/Electronics/Software.
DATA CENTER: công suất MW, pipeline MW, Tier III vs IV, major players, giá colocation USD/kW/tháng, AI hyperscaler expansion.

[II] PLAYER & DỰ ÁN NỔI BẬT (3–5 tin): KCN mới phê duyệt, FDI >100M USD, data center mới, M&A industrial.

[III] PHÁP LÝ: quy hoạch KCN đến 2030, ưu đãi thuế FDI (global minimum tax), data center (an ninh mạng, data localization), KCN sinh thái.

[IV] XU HƯỚNG QUỐC TẾ: China+1, semiconductor supply chain VN, AI infrastructure boom, green industrial park, McKinsey "Future of Asia Manufacturing".

[V] POV CHIẾN LƯỢC:
A. Shift từ labor-cost sang ecosystem advantage; phân hóa KCN thường vs high-tech; data center = critical infra. 3–4 shifts với dự báo 2025–2030.
B. Where to Play: tỉnh/vùng nào cho KCN/tech park/data center? Phân khúc tenant nào highest-value? Format nào demand-supply gap tốt nhất?
C. How to Win: KCN developer cần gì để thu hút FDI chất lượng cao? Data center moat thực sự? Cluster effect strategy.

Liệt kê nguồn. Nếu thiếu dữ liệu → ghi rõ.
""",
}

# ── Email HTML wrapper ────────────────────────────────────────────────────────
EMAIL_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head><meta charset="UTF-8"></head>
<body style="font-family:'Segoe UI',Arial,sans-serif;font-size:14px;color:#1a1a1a;max-width:820px;margin:0 auto;background:#f9f9f9;padding:20px;">
<div style="background:#1a2744;color:#fff;padding:18px 24px;border-radius:8px 8px 0 0;">
  <h1 style="margin:0;font-size:20px;">{session_label} DEEP DIVE</h1>
  <p style="margin:4px 0 0;font-size:13px;color:#a8bde8;">{date_str} | Tổng hợp bởi Claude | Nguồn: Savills · CBRE · JLL · Cushman & Wakefield</p>
</div>
<div style="background:#fff;padding:20px 24px;border-radius:0 0 8px 8px;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
{body}
<div style="margin-top:16px;font-size:11px;color:#9ca3af;text-align:center;border-top:1px solid #f3f4f6;padding-top:10px;">
  Tổng hợp tự động bởi Claude · claude-sonnet-4-6 · {date_str} 07:30 AM
</div>
</div>
</body>
</html>"""


def get_vietnam_now() -> datetime:
    return datetime.now(VN_TZ)


def should_run_today(weekday: int) -> bool:
    """Return True only for Mon–Thu (0–3)."""
    return weekday in SESSIONS


def build_subject(session_label: str, asset_class: str, now: datetime) -> str:
    thu_map = {0: "Thứ 2", 1: "Thứ 3", 2: "Thứ 4", 3: "Thứ 5"}
    thu_str = thu_map[now.weekday()]
    date_str = now.strftime("%d/%m/%Y")
    return f"{asset_class} Deep Dive — {thu_str}, {date_str}"


def markdown_to_simple_html(text: str) -> str:
    """Minimal markdown → HTML conversion for email body."""
    import re
    # Headers
    text = re.sub(r'^### (.+)$', r'<h3 style="font-size:14px;color:#2563eb;">\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'<h2 style="font-size:15px;color:#1a2744;border-bottom:2px solid #1a2744;padding-bottom:6px;">\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)$', r'<h1 style="font-size:16px;color:#1a2744;">\1</h1>', text, flags=re.MULTILINE)
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Bullet points
    lines = text.split('\n')
    out, in_ul = [], False
    for line in lines:
        if line.startswith('- ') or line.startswith('• '):
            if not in_ul:
                out.append('<ul style="line-height:1.9;">')
                in_ul = True
            out.append(f'<li>{line[2:]}</li>')
        else:
            if in_ul:
                out.append('</ul>')
                in_ul = False
            out.append(f'<p style="margin:6px 0;">{line}</p>' if line.strip() else '')
    if in_ul:
        out.append('</ul>')
    return '\n'.join(out)


def generate_report(weekday: int, now: datetime) -> str:
    """Call Claude API to generate the analysis report."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    thu_map = {0: "Thứ 2", 1: "Thứ 3", 2: "Thứ 4", 3: "Thứ 5"}
    date_str = f"{thu_map[weekday]}, {now.strftime('%d/%m/%Y')}"
    prompt = SESSION_PROMPTS[weekday].format(date_str=date_str)

    # Use prompt caching for the large system prompt
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        system=[
            {
                "type": "text",
                "text": (
                    "Bạn là chuyên gia chiến lược bất động sản cấp senior với 20 năm kinh nghiệm, "
                    "từng làm việc tại McKinsey, CBRE và Savills. Phân tích theo chuẩn tư vấn chiến lược: "
                    "số liệu cụ thể, insight có chiều sâu, hành động được. Không viết chung chung. "
                    "Mỗi bullet phải có số liệu hoặc ví dụ cụ thể. Nếu thiếu dữ liệu thực tế gần nhất, "
                    "hãy nêu rõ 'Chưa có cập nhật — số liệu gần nhất: [ngày] từ [nguồn]' thay vì bịa số liệu."
                ),
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def send_via_gmail(subject: str, html_body: str, recipient: str = "nxbach1509@gmail.com") -> None:
    """Send email using Gmail API with OAuth2 credentials from environment."""
    token_json = os.environ.get("GMAIL_TOKEN_JSON")
    if not token_json:
        raise EnvironmentError("GMAIL_TOKEN_JSON environment variable not set.")

    import json
    token_data = json.loads(token_json)
    creds = Credentials(
        token=token_data.get("token"),
        refresh_token=token_data.get("refresh_token"),
        token_uri=token_data.get("token_uri", "https://oauth2.googleapis.com/token"),
        client_id=token_data.get("client_id"),
        client_secret=token_data.get("client_secret"),
        scopes=token_data.get("scopes", ["https://www.googleapis.com/auth/gmail.send"]),
    )

    service = build("gmail", "v1", credentials=creds)
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["To"] = recipient
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    service.users().messages().send(userId="me", body={"raw": raw}).execute()
    print(f"[OK] Email sent: {subject}")


def main() -> None:
    now = get_vietnam_now()
    weekday = now.weekday()

    if not should_run_today(weekday):
        day_names = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ Nhật"]
        print(f"[SKIP] {day_names[weekday]} — không có báo cáo hôm nay.")
        sys.exit(0)

    session_code, asset_class = SESSIONS[weekday]
    thu_map = {0: "Thứ 2", 1: "Thứ 3", 2: "Thứ 4", 3: "Thứ 5"}
    date_str = f"{thu_map[weekday]}, {now.strftime('%d/%m/%Y')}"

    print(f"[START] {session_code}: {asset_class} — {date_str}")

    report_md = generate_report(weekday, now)
    report_html = markdown_to_simple_html(report_md)

    full_html = EMAIL_HTML_TEMPLATE.format(
        session_label=f"{session_code}: {asset_class}",
        date_str=date_str,
        body=report_html,
    )

    subject = build_subject(session_code, asset_class, now)
    send_via_gmail(subject, full_html)


if __name__ == "__main__":
    main()
