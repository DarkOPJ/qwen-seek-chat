import json
import os
import sys

import pinject
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from loguru import logger as loguru_logger

# Add "app" root to PYTHONPATH so we can import from app i.e. from app import create_app.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app  # noqa: E402
from app.core.exceptions import AppExceptionCase  # noqa: E402
from config import settings  # noqa: E402

if __name__ == "__main__":
    loguru_logger.info("CONNECTING TO KAFKA SERVER")
    try:
        consumer = KafkaConsumer(
            bootstrap_servers=settings.kafka_bootstrap_servers.split("|"),
            auto_offset_reset="earliest",
            group_id=settings.kafka_subscription,
            security_protocol=settings.kafka_security_protocol,
            sasl_mechanism=settings.kafka_sasl_mechanism,
            sasl_plain_username=settings.kafka_server_username,
            sasl_plain_password=settings.kafka_server_password,
            enable_auto_commit=False,
        )
    except KafkaError as exc:
        loguru_logger.error(f"KafkaError({exc}) occurred while connecting")
    else:
        subscription = settings.kafka_subscription.split("|")
        consumer.subscribe(subscription)
        loguru_logger.info(f"Topic Subscription List: {subscription}")
        loguru_logger.info("AWAITING MESSAGES\n")

        app = create_app()
        # Create Application before importing from app
        from app.controllers.v1 import SyncResourceController
        from app.repositories import SyncResourceRepository

        for msg in consumer:
            data = json.loads(msg.value)
            loguru_logger.info(
                f"KafkaRequest[{settings.app_name}({settings.app_env}) | Received]\n"
            )
            obj_graph = pinject.new_object_graph(
                modules=None, classes=[SyncResourceController, SyncResourceRepository]
            )
            resource_controller: SyncResourceController = obj_graph.provide(
                SyncResourceController
            )
            try:
                resource_controller.create_resource(obj_data=data)
                loguru_logger.info(
                    f"KafkaRequest[{settings.app_name}({settings.app_env}) | Successful]\n"  # noqa
                )
            except AppExceptionCase:
                loguru_logger.error(
                    f"KafkaRequest[{settings.app_name}({settings.app_env}) | Failed]\n"  # noqa
                )
            consumer.commit()
            loguru_logger.info(
                f"KafkaRequest[{settings.app_name}({settings.app_env}) | Offset_Commit_Successful]"  # noqa
            )
