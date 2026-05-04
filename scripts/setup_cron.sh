#!/usr/bin/env bash
# setup_cron.sh — Cài đặt cron job cho AI Weekly Report
# Chạy: bash scripts/setup_cron.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PYTHON_SCRIPT="$PROJECT_ROOT/routines/ai-weekly/report_generator.py"
PYTHON_BIN="${PYTHON_BIN:-$(which python3 2>/dev/null || echo python3)}"
LOG_FILE="$PROJECT_ROOT/logs/cron_runner.log"
CRON_MARKER="ai-weekly-report"

# Kiểm tra file script tồn tại
if [[ ! -f "$PYTHON_SCRIPT" ]]; then
    echo "ERROR: Không tìm thấy $PYTHON_SCRIPT"
    exit 1
fi

chmod +x "$PYTHON_SCRIPT"

# Cron expression: 7:30 AM mỗi thứ Sáu (day-of-week = 5)
CRON_SCHEDULE="30 7 * * 5"
CRON_CMD="$PYTHON_BIN $PYTHON_SCRIPT >> $LOG_FILE 2>&1"
CRON_JOB="$CRON_SCHEDULE $CRON_CMD"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  AI Weekly Report — Cron Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Python  : $PYTHON_BIN"
echo "Script  : $PYTHON_SCRIPT"
echo "Schedule: Thứ Sáu, 07:30 AM ($CRON_SCHEDULE)"
echo "Log     : $LOG_FILE"
echo ""

# Phương án 1: crontab (ưu tiên)
if command -v crontab &>/dev/null; then
    echo "Cài cron job vào crontab..."

    # Xoá entry cũ nếu tồn tại
    if crontab -l 2>/dev/null | grep -q "$CRON_MARKER"; then
        echo "  Xoá entry cũ..."
        crontab -l 2>/dev/null | grep -v "$CRON_MARKER" | crontab -
    fi

    # Thêm cron job mới (kèm marker comment)
    (
        crontab -l 2>/dev/null || true
        echo "# $CRON_MARKER — AI Weekly Report Generator"
        echo "$CRON_JOB"
    ) | crontab -

    echo "✓ Cron job đã thêm vào crontab:"
    echo "  $CRON_JOB"
    echo ""
    echo "Kiểm tra: crontab -l"

# Phương án 2: /etc/cron.d/ (nếu có quyền)
elif [[ -d "/etc/cron.d" ]] && [[ $EUID -eq 0 ]]; then
    CRON_FILE="/etc/cron.d/ai-weekly-report"
    echo "Cài cron job vào /etc/cron.d/..."
    cat > "$CRON_FILE" <<EOF
# AI Weekly Report — tự động chạy thứ Sáu 7:30 AM
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
$CRON_SCHEDULE root $CRON_CMD
EOF
    chmod 644 "$CRON_FILE"
    echo "✓ Cron job đã tạo tại $CRON_FILE"
    echo "Kiểm tra: cat $CRON_FILE"

# Phương án 3: Hướng dẫn thủ công
else
    echo "⚠️  Không tìm thấy 'crontab'. Thêm thủ công bằng cách chạy:"
    echo ""
    echo "  crontab -e"
    echo ""
    echo "Sau đó thêm dòng sau vào cuối file:"
    echo ""
    echo "  # AI Weekly Report"
    echo "  $CRON_JOB"
    echo ""
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Chạy thử ngay (dry-run, không gửi email):"
echo "  python3 $PYTHON_SCRIPT --dry-run"
echo ""
echo "  Chạy đầy đủ (gửi email thật):"
echo "  python3 $PYTHON_SCRIPT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
