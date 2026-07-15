from amqp import exceptions as amqp_exc
from kombu import Exchange, Queue
from kombu import exceptions as kombu_exc

from app.celery_app import celery
from app.core.exceptions import AppException


def send_to_recovery_queue(
    data: dict,
    queue: str,
    task_name: str = "task name",
    queue_type: str = "direct",
):
    data["metadata"] = {**data.get("metadata", {}), "queue": queue}
    try:
        celery.send_task(
            task_name,
            kwargs=data,
            queue=Queue(
                name=queue,
                exchange=Exchange(queue, type=queue_type),
                routing_key=queue,
            ).name,
        )
    except (kombu_exc.KombuError, amqp_exc.AMQPError) as exc:
        raise AppException.InternalServerException(
            error_message=f"CeleryBrokerError({exc})",
            context=f"CeleryBrokerError({exc})",
        )
