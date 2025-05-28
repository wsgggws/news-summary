#!/usr/bin/env bash
set -euo pipefail

echo "🛑 正在停止 Celery 进程..."

pids=$(pgrep -f "celery" || true) # 加上 || true，防止无进程时脚本退出

if [[ -z "$pids" ]]; then
  echo "⚠️  未发现正在运行的 Celery 进程"
  exit 0
fi

echo "找到 Celery 进程 PID: $pids"

for pid in $pids; do
  echo "🔪 尝试终止 PID: $pid"
  if kill "$pid"; then
    echo "✅ 成功发送终止信号给 PID: $pid"
  else
    echo "⚠️ 无法终止 PID: $pid，尝试强制杀死"
    kill -9 "$pid" || echo "❌ 强制杀死失败，检查权限"
  fi
done

echo "✅ Celery 进程已全部停止"
