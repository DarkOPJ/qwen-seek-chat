from config import settings

broker_url = f"amqp://{settings.rmq_user}:{settings.rmq_password}@{settings.rmq_server}:{settings.rmq_port}/{settings.rmq_vhost}"  # noqa
if settings.redis_sentinel:
    result_backend = f"sentinel://:{settings.redis_password}@{settings.redis_sentinel}/0"
    result_backend_transport_options = {
        "master_name": settings.redis_sentinel_master,
        "sentinel_kwargs": {"password": settings.redis_password},
    }
else:
    result_backend = f"redis://:{settings.redis_password}@{settings.redis_server}:{settings.redis_port}/0"  # noqa
broker_transport_options = {"queue_order_strategy": "priority"}
broker_connection_max_retries = 5
task_reject_on_worker_lost = True
