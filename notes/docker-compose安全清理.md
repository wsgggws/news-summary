# docker compose 安全清理

- ✅ 清除未使用的 container、image、volume, netword
- 🚫 不影响正在运行的服务
- ✅ 安全操作

## 清理过程

```sh
# 停止的容器
docker container prune -f

# 悬空镜像
docker image prune -f

# 未挂载的卷（安全） 会释放较多的磁盘空间
docker volume prune -f

# 无用网络
docker network prune -f

```

## 🔎 建议定期查看状态

```sh
# 查看所有容器（含停止）
docker ps -a

# 查看所有 volume
docker volume ls

# 查看未使用的 volume
docker volume ls -f dangling=true

# 查看磁盘空间使用情况
docker system df

```

## 进一步清理 dangling 的 volume

```sh
# !!! 删除前你可以再检查确认
docker volume ls -f dangling=true

docker volume ls -f dangling=true -q | xargs -r docker volume rm
```
