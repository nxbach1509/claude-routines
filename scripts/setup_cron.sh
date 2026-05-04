#!/usr/bin/env bash
# setup_cron.sh — Cài đặt cron job cho AI Weekly Report
# Chạy: bash scripts/setup_cron.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PYTHON_SCRIPT="$PROJECT_ROOT/routines/ai-weekly/report_generator.py"
PYTHON_BIN="${PYTHON_BIN:-$(which python3)}"
LOG_FILE="$PROJECT_ROOT/logs/cron_runner.log"

# Kiểm tra file script tồn tại
if [[ ! -f "$PYTHON_SCRIPT" ]]; then
    echo "ERROR: Không tìm thấy $PYTHON_SCRIPT"
    exit 1
fi

# Đảm bảo script có quyền thực thi
chmod +x "$PYTHON_SCRIPT"

# Cron expression: 7:30 AM mỗi thứ Sáu (day-of-week = 5)
CRON_SCHEDULE="30 7 * * 5"
CRON_CMD="$PYTHON_BIN $PYTHON_SCRIPT >> $LOG_FILE 2>&1"
CRON_JOB="$CRON_SCHEDULE $CRON_CMD"
CRON_MARKER="ai-weekly-report"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  AI Weekly Report — Cron Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Python  : $PYTHON_BIN"
echo "Script  : $PYTHON_SCRIPT"
echo "Schedule: Thứ Sáu, 07:30 AM ($CRON_SCHEDULE)"
echo "Log     : $LOG_FILE"
echo ""

# Xoá entry cũ nếu tồn tại
if crontab -l 2>/dev/null | grep -q "$CRON_MARKER"; then
    echo "Đang xoá cron job cũ..."
    crontab -l 2>/dev/null | grep -v "$CRON_MARKER" | crontab -
fi

# Thêm cron job mới (kèm marker comment)
(
    crontab -l 2>/dev/null || true
    echo "# $CRON_MARKER — AI Weekly Report Generator"
    echo "$CRON_JOB"
) | crontab -

echo "✓ Cron job đã được thêm:"
echo "  $CRON_JOB"
echo ""
echo "Kiểm tra bằng lệnh: crontab -l"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Chạy thử ngay (không cần đợi đến thứ Sáu):"
echo "  python3 $PYTHON_SCRIPT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
