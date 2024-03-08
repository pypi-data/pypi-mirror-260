from celery import Celery
from ai_butler_sdk.settings import settings

from celery.signals import worker_shutdown, worker_process_init
from ai_butler_sdk.apis.client import worker_online, worker_offline


@worker_process_init.connect
def on_worker_process_init(**kwargs):
    """celery worker启动信号"""
    is_success = worker_online(
        settings.CELERY_WORKER_NAME, settings.CELERY_WORKER_LISTEN_QUEUE, settings.CELERY_WORKER_CONCURRENCY
    )
    if not is_success:
        exit()


@worker_shutdown.connect
def on_worker_shutdown(**kwargs):
    """celery worker终止信号"""
    worker_offline(settings.CELERY_WORKER_NAME)


def create_celery_app():
    broker_url = settings.CELERY_BROKER_URL

    app = Celery("ai_butler", broker=broker_url, broker_connection_retry_on_startup=False)
    app.autodiscover_tasks()
    return app


def start_worker(app):
    worker = app.Worker(
        concurrency=settings.CELERY_WORKER_CONCURRENCY,  # 设置并发数
        loglevel=settings.CELERY_WORKER_LOGGER_LEVEL,
        queues=[settings.CELERY_WORKER_LISTEN_QUEUE],  # 指定监听队列
    )
    worker.start()


celery_app = create_celery_app()
