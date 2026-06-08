#!/bin/bash
# Wi-Fi Rec AI Server — DGX-Spark 시작 스크립트
# 실행: bash start.sh

set -e

# ── 1. 가상환경 ─────────────────────────────────────────────────
if [ ! -d ".venv" ]; then
  echo "[setup] 가상환경 생성..."
  python3 -m venv .venv
fi

source .venv/bin/activate

# ── 2. 의존성 설치 ────────────────────────────────────────────────
echo "[setup] 의존성 설치..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

# ── 3. 포트 설정 (기본 8000) ─────────────────────────────────────
PORT=${PORT:-8000}

# ── 4. 서버 실행 ─────────────────────────────────────────────────
echo ""
echo "========================================"
echo "  AI Server starting on 0.0.0.0:${PORT}"
echo "  Docs: http://$(hostname -I | awk '{print $1}'):${PORT}/docs"
echo "========================================"
echo ""

uvicorn main:app --host 0.0.0.0 --port "${PORT}" --workers 1
