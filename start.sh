#!/bin/bash
# start.sh — SDD 平台启动脚本

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
export SDD_PROJECT_REPO="${1:-$(pwd)}"
export SDD_DATA_DIR="${SCRIPT_DIR}/data"

echo "SDD Platform"
echo "  Project repo: $SDD_PROJECT_REPO"
echo "  Data dir:     $SDD_DATA_DIR"

# 导入 skills（如需要）
cd "$SCRIPT_DIR/backend"
python3 scripts/import_skills.py

# 启动后端
echo "Starting backend on :8000..."
uvicorn main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# 启动前端
echo "Starting frontend on :5173..."
cd "$SCRIPT_DIR/frontend"
npm run dev &
FRONTEND_PID=$!

echo ""
echo "SDD Platform running:"
echo "  Web: http://localhost:5173"
echo "  API: http://localhost:8000/api/health"
echo ""
echo "Press Ctrl+C to stop"

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" INT TERM
wait
