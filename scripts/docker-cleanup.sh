#!/usr/bin/env bash

set -euo pipefail

echo "🧹 正在进行强力 Docker 清理..."

# 停止的容器
echo "1. 删除所有已停止的容器..."
docker container prune -f

# 悬空镜像（dangling: <none> 标签）
echo "2. 删除所有悬空镜像（无标签 <none>）..."
dangling_images=$(docker images -f "dangling=true" -q)
if [ -n "$dangling_images" ]; then
  docker rmi "${dangling_images}" || true
else
  echo "  ➤ 无悬空镜像需要删除"
fi

# 未挂载的卷
echo "3. 删除所有未挂载的卷..."
docker volume prune -f

# 无用网络
echo "4. 删除所有无用的网络..."
docker network prune -f

# 构建缓存（可选，如果你用 buildx）
echo "5. 删除 buildx 缓存（如果存在）..."
docker builder prune -f || true

echo "6. 删除所有匿名卷 ..."
docker volume ls -qf dangling=true | xargs -r docker volume rm

echo "✅ 强力清理完成！"
