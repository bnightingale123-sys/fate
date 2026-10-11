#!/bin/bash
# =============================================
# yourfate.xyz — 紫微斗数解密服务 启动脚本
# =============================================
set -e

cd "$(dirname "$0")"
PROJECT_DIR="$(pwd)"

# ----- 加载 .env -----
if [ -f .env ]; then
    set -a
    source .env
    set +a
    echo "[OK] .env loaded"
else
    echo "[WARN] .env not found — using placeholder keys"
fi

# ----- 安装依赖 -----
echo "[*] Installing Python dependencies..."
pip install -r requirements_web.txt -q

# ----- 初始化数据库 -----
echo "[*] Database ready (auto-created on first run)"

# ----- 启动服务 -----
PORT="${PORT:-5000}"
echo ""
echo "========================================"
echo "  yourfate.xyz server starting"
echo "  Port: $PORT"
echo "  Domain: ${DOMAIN:-https://yourfate.xyz}"
echo "========================================"

# 优先用 gunicorn（生产），否则用 Flask 自带
if command -v gunicorn &> /dev/null; then
    echo "[*] Using gunicorn (production mode)"
    exec gunicorn --bind 127.0.0.1:$PORT \
        --workers 2 \
        --timeout 120 \
        --access-logfile - \
        --error-logfile - \
        server:app
else
    echo "[WARN] gunicorn not installed; using Flask dev server"
    echo "       Install gunicorn: pip install gunicorn"
    exec python server.py
fi
