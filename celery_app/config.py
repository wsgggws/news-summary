from urllib.parse import quote_plus

from celery.schedules import crontab

from settings import settings

passwd = quote_plus(settings.redis.PASSWORD or "")
# Broker 配置（任务队列）
broker_url = f"redis://:{passwd}@{settings.redis.HOST}:{settings.redis.PORT}/{settings.redis.BROKER_NUM}"
# 结果存储（任务执行结果）
result_backend = f"redis://:{passwd}@{settings.redis.HOST}:{settings.redis.PORT}/{settings.redis.BACKEND_NUM}"

# 指定任务序列化方式
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]

# 时区设置
timezone = "Asia/Shanghai"
enable_utc = False

# 导入任务模块（可选，如果没使用 autodiscover_tasks）
# import_modules = ("celery_app.tasks.rss_crawler",)

# Beat 调度器
beat_schedule = {
    "dispatch_rss_fetch": {
        "task": "celery_app.tasks.rss_dispatcher.dispatch_all_feeds",
        "schedule": crontab(minute="*/1"),  # 每1分钟执行
        "args": (),
    },
}

# worker 并发控制（这里不一定要设置，推荐使用 CLI 参数）
# worker_concurrency = 4

# 默认队列
task_default_queue = "default"

# 可选：结果过期时间（秒）
result_expires = 3600

# task_acks_late = True	任务异常时重新投递（消息幂等时建议开启）
# worker_max_tasks_per_child = 100	每个 worker 进程处理的最大任务数，防止内存泄漏
# task_time_limit = 300	单个任务最大执行时间
# broker_connection_retry_on_startup = True	防止 Celery 启动时 Broker 未启动就挂掉
