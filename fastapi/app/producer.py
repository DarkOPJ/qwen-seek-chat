import json
import threading

from kafka import KafkaProducer
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.core.exceptions import AppException
from config import settings


class KafkaPublisher:
    _instance, _lock = None, threading.Lock()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = KafkaProducer(
                        bootstrap_servers=settings.kafka_bootstrap_servers.split("|"),
                        value_serializer=cls.json_serializer,
                        acks="all",
                        retries=5,
                        security_protocol=settings.kafka_security_protocol,
                        sasl_mechanism=settings.kafka_sasl_mechanism,
                        sasl_plain_username=settings.kafka_server_username,
                        sasl_plain_password=settings.kafka_server_password,
                    )
        return cls._instance

    @classmethod
    def json_serializer(cls, data):
        return json.dumps(data).encode("UTF-8")

    @classmethod
    def get_partition(cls, key, all, available):
        return 0

    @classmethod
    @retry(
        retry=retry_if_exception_type(AppException.BadRequestException),
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, max=30),
        reraise=True,
    )
    def publish_to_kafka(cls, topic, value):
        try:
            producer = cls.get_instance()
            producer.send(topic=topic, value=value).add_callback(
                cls.on_success
            ).add_errback(cls.on_failure)
            producer.flush(timeout=10)
        except Exception as exc:  # noqa
            cls.close()
            raise AppException.BadRequestException(error_message=f"KafkaError({exc})")

    @classmethod
    def on_success(cls, record):
        pass

    @classmethod
    def on_failure(cls, exc):
        raise AppException.BadRequestException(error_message=f"KafkaError({exc})")

    @classmethod
    def close(cls):
        if cls._instance:
            cls._instance.close()
            cls._instance = None
