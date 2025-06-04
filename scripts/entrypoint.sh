#!/bin/sh
set -e

echo "🚀 Starting FastAPI application (HTTP only, SSL handled by Nginx)..."

# 启动 FastAPI (监听 HTTP)
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4 # 可选 --workers
