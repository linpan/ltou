from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "move_worker",
    backend=settings.REDIS_URL,
    broker=settings.RABBIT_URI
)
# fixme register your task here...
# # load task modules from all registered
celery_app.conf.task_routes = {
    "app.tasks": "test-queue"}

# specify result serialization format
celery_app.config['CELERY_TASK_SERIALIZER'] = 'json'
# specify task serialization format
celery_app.config['CELERY_RESULT_SERIALIZER'] = 'json'

# worker concurrency level
celery_app.config['CELERYD_CONCURRENCY'] = 8
# worker pool implementation

celery_app.config['CELERYD_POOL'] = "gevent"
# worker process memory limit (in MB)
celery_app.config['CELERYD_MAX_TASK_MEMORY_SOFT_LIMIT'] = 1024
celery_app.config['CELERYD_MAX_TASK_MEMORY_HARD_LIMIT'] = 2048

celery_app.config['WORKER_MAX_TASKS_PER_CHILD'] = 100
celery_app.config['worker_max_memory_per_child'] = 64000  # MB 64

# timezone for scheduling tasks
celery_app.config["CELERY_TIMEZONE"] = "UTC"
celery_app.config["TASK_TRACK_STARTED"] = True
