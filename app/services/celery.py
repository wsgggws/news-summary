from celery import Celery

celery_app = Celery(
    "rss_crawler",
    broker="redis://localhost:6379/0",
)

# 自定义数据库后端（我们自己写一个存任务状态）
celery_app.conf.update(
    task_track_started=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
)
