# claude-routines

Tập hợp các routine tự động chạy bằng Claude API. Hiện tại bao gồm:

## Routines

### AI Weekly Report (`routines/ai-weekly/`)

Tổng hợp các phát triển AI quan trọng trong 7 ngày qua, gửi email báo cáo mỗi thứ Sáu lúc 7:30 AM.

**Cấu trúc:**
```
routines/ai-weekly/
├── report_generator.py   # Script chính (Anthropic SDK + web search + Gmail SMTP)
└── prompt_template.md    # Template prompt với cấu trúc báo cáo 5 layer
```

---

## Cài đặt & Chạy

### 1. Cài dependencies

```bash
pip install -r requirements.txt
```

### 2. Cấu hình environment variables

```bash
cp .env.example .env
# Mở .env và điền:
#   ANTHROPIC_API_KEY — key từ console.anthropic.com
#   GMAIL_USER        — Gmail dùng để gửi
#   GMAIL_APP_PASSWORD — App Password 16 ký tự (không phải mật khẩu Gmail)
#   TAVILY_API_KEY    — (tuỳ chọn) key từ app.tavily.com để tìm kiếm tốt hơn
```

**Cách tạo Gmail App Password:**
1. Bật 2-Step Verification tại https://myaccount.google.com/security
2. Vào https://myaccount.google.com/apppasswords
3. Chọn app "Mail", đặt tên "AI Weekly Bot"
4. Copy 16 ký tự password → dán vào `GMAIL_APP_PASSWORD`

### 3. Chạy thử

```bash
python3 routines/ai-weekly/report_generator.py
```

### 4. Cài cron job (tự động chạy thứ Sáu 7:30 AM)

```bash
bash scripts/setup_cron.sh
```

Kiểm tra cron đã được thêm:
```bash
crontab -l
```

---

## Kiến trúc

```
Cron (Thứ Sáu, 07:30 AM)
    └─ report_generator.py
            ├─ Anthropic API (claude-sonnet-4-6)
            │       └─ Tool use: web_search
            │               ├─ Tavily API (nếu có key)  ← chính xác hơn
            │               └─ DuckDuckGo              ← fallback, không cần key
            └─ Gmail SMTP → nxbach1509@gmail.com
```

**Khung phân tích:** Johnson Wang 4-Layer AI Stack
- Layer 1: Hardware, Chip, Data Center & Infrastructure
- Layer 2: Data, Cloud & Hyperscaler
- Layer 3: Models & Research
- Layer 4: Applications (BĐS, Ngân hàng, Sân bay, Giáo dục, Y tế, Dịch vụ)
- Layer 5: POV, Scoreboard & What to Watch

## Logs

Logs được lưu tại `logs/` directory:
- `logs/ai_weekly_YYYYMMDD.log` — log từng lần chạy
- `logs/ai_weekly_weekWW_YYYY.txt` — bản sao báo cáo local
- `logs/cron_runner.log` — output từ cron
