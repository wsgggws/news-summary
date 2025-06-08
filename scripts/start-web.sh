#!/usr/bin/env bash
set -euo pipefail

echo "🚀 Starting FastAPI application."

# 启动 FastAPI (监听 HTTP)
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-level info
