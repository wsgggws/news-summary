#!/bin/bash
set -e

DOCKER_ROOT="/var/lib/docker"
echo "📦 正在统计 $DOCKER_ROOT 各类子目录使用情况..."
echo

subdirs=(overlay2 volumes containers image buildkit tmp network)
printf "📊 Docker 子目录空间总览\n"
printf "%-15s | %-8s | %-10s | %s\n" "目录名" "目录数" "总大小" "路径"
echo "-------------------------------------------------------------"

total_bytes=0

for dir in "${subdirs[@]}"; do
  full_path="$DOCKER_ROOT/$dir"
  if [ -d "$full_path" ]; then
    count=$(find "$full_path" -mindepth 1 -maxdepth 1 2>/dev/null | wc -l)
    size=$(du -sh "$full_path" 2>/dev/null | awk '{print $1}')
    bytes=$(du -sb "$full_path" 2>/dev/null | awk '{print $1}')
    total_bytes=$((total_bytes + bytes))
    printf "%-15s | %-8s | %-10s | %s\n" \
      "${dir:-<none>}" \
      "${count:-0}" \
      "${size:-0B}" \
      "${full_path:-<missing>}"
  else
    printf "%-15s | %-8s | %-10s | %s\n" "$dir" "0" "0B" "$full_path (不存在)"
  fi
done

# 总体大小换算显示
total_gb=$(awk "BEGIN {printf \"%.1fGiB\", $total_bytes / (1024*1024*1024)}")
echo -e "\n🧮 合计空间使用: $total_gb"

echo
echo "📈 Top 5 Docker 占用空间目录（大于 100MB）"
du -h "$DOCKER_ROOT"/* 2>/dev/null | sort -hr | awk '$1 ~ /[0-9\.]+[MG]/' | head -n 5

echo
echo "🧾 容器日志文件大小 (前5大 *.log)"
find "$DOCKER_ROOT/containers" -name "*.log" -type f 2>/dev/null |
  xargs du -h 2>/dev/null | sort -hr | head -n 5

echo
echo "🐳 Docker System 使用情况 (docker system df)"
docker system df

echo -e "\n✅ 完成分析."
