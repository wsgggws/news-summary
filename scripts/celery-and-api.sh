nohup celery -A celery_app beat --loglevel=info 2>&1 &

nohup celery -A celery_app worker --pool=threads --concurrency=1 --loglevel=info 2>&1 &
nohup celery -A celery_app worker --pool=threads --concurrency=1 --loglevel=info 2>&1 &

uvicorn src.main:app --host 0.0.0.0 --port 8000
