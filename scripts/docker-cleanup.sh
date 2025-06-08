#!/usr/bin/env bash

set -euo pipefail

echo "🧹 正在进行强力 Docker 清理..."

# 停止的容器
echo "1. 删除所有已停止的容器..."
docker container prune -f

# 未挂载的卷
echo "2. 删除所有未挂载的卷..."
docker volume prune -f

# 无用网络
echo "3. 删除所有无用的网络..."
docker network prune -f

echo "4. 删除所有匿名卷 ..."
docker volume ls -qf dangling=true | xargs -r docker volume rm

echo "✅ 强力清理完成！"
