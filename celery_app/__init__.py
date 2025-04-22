from celery import Celery

celery_app = Celery("rss_crawler")

celery_app.config_from_object("celery_app.config")
celery_app.autodiscover_tasks(["celery_app.tasks.rss_crawler", "celery_app.tasks.rss_dispatcher"])
