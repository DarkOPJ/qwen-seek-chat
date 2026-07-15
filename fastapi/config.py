import os
import enum
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class SortResultEnum(enum.Enum):
    asc = "asc"
    desc = "desc"


DEVELOPMENT_ENVIRONMENT = "development"
UAT_ENVIRONMENT = "uat"
PRODUCTION_ENVIRONMENT = "production"
TESTING_ENVIRONMENT = "testing"
ENV_ERROR = "invalid environment: {}"
APPLICATION_NAME = "FastApi Template"
LOG_HEADER = f"{APPLICATION_NAME} Log"


class BaseConfig(BaseSettings):
    # general application settings
    app_name: str = "FastApi Template"
    app_env: str = ""
    app_root: str = str(Path(__file__).parent)
    log_header: str = f"{app_name} Log"
    maintainer_mail_address: str = ""
    cors_origins: str = "*"
    # database server configuration
    db_type: str = "sqlite"  # sqlite or postgres
    sqlite_db_path: str = "./data/qwen_chat.db"
    db_host: str = ""
    db_user: str = ""
    db_password: str = ""
    db_name: str = ""
    db_port: int = 5432
    db_ssl: bool = True
    db_connection_pool: bool = True
    db_async_connection: bool = False
    # redis server configuration
    redis_server: str = ""
    redis_port: int = 6379
    redis_password: str = ""
    redis_db: int = 0
    redis_sentinel: str = ""
    redis_sentinel_master: str = ""
    redis_sentinel_timeout: float = 0.1
    # rabbitmq server config
    rmq_server: str = ""
    rmq_port: int = 5672
    rmq_user: str = ""
    rmq_password: str = ""
    rmq_vhost: str = ""
    # mail server configuration
    mail_server: str = ""
    mail_server_port: str = ""
    default_mail_sender: str = ""
    default_mail_sender_address: str = ""
    default_mail_sender_password: str = ""
    # keycloak configuration
    keycloak_client_id: str = ""
    keycloak_client_secret: str = ""
    keycloak_uri: str = ""
    keycloak_realm: str = ""
    keycloak_realm_admin_username: str = ""
    keycloak_realm_admin_password: str = ""
    jwt_algorithms: list = ["HS256", "RS256"]
    jwt_public_key: str = ""
    # kafka configuration
    kafka_bootstrap_servers: str = ""
    kafka_server_username: str = ""
    kafka_server_password: str = ""
    kafka_subscription: str = ""
    kafka_security_protocol: str = "SASL_PLAINTEXT"
    kafka_sasl_mechanism: str = "SCRAM-SHA-512"
    # Ollama configuration
    ollama_host: str = "http://localhost:11434"
    ollama_default_models: list = ["qwen3:1.7b", "deepseek-r1:1.5b"]
    ollama_timeout: int = 120

    @property
    def SQLALCHEMY_DATABASE_URI(self):  # noqa
        if self.db_type == "sqlite":
            if self.db_async_connection:
                return f"sqlite+aiosqlite:///{self.sqlite_db_path}"
            return f"sqlite:///{self.sqlite_db_path}"
        if self.db_async_connection:
            return "postgresql+asyncpg://{db_user}:{password}@{host}:{port}/{db_name}".format(  # noqa
                db_user=self.db_user,
                host=self.db_host,
                password=self.db_password,
                port=self.db_port,
                db_name=self.db_name,
            )
        return "postgresql+psycopg2://{db_user}:{password}@{host}:{port}/{db_name}".format(  # noqa
            db_user=self.db_user,
            host=self.db_host,
            password=self.db_password,
            port=self.db_port,
            db_name=self.db_name,
        )

    @property
    def SQLITE_CONNECT_ARGS(self):
        """SQLite-specific connect arguments."""
        if self.db_type == "sqlite":
            return {"check_same_thread": False}
        return {}

    class Config:
        env_file = ".env"
        extra = "allow"


class DevelopmentConfig(BaseConfig):
    pass


class UatConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    test_db_host: str = ""
    test_db_user: str = ""
    test_db_password: str = ""
    test_db_name: str = ""
    test_db_port: str = ""
    db_ssl: bool = False
    redis_db: int = 1

    @property
    def SQLALCHEMY_DATABASE_URI(self):  # noqa
        if self.db_type == "sqlite":
            if self.db_async_connection:
                return f"sqlite+aiosqlite:///{self.sqlite_db_path}"
            return f"sqlite:///{self.sqlite_db_path}"
        if self.db_async_connection:
            return "postgresql+asyncpg://{db_user}:{password}@{host}:{port}/{db_name}".format(  # noqa
                db_user=self.test_db_user,
                host=self.test_db_host,
                password=self.test_db_password,
                port=self.test_db_port,
                db_name=self.test_db_name,
            )
        return "postgresql+psycopg2://{db_user}:{password}@{host}:{port}/{db_name}".format(  # noqa
            db_user=self.test_db_user,
            host=self.test_db_host,
            password=self.test_db_password,
            port=self.test_db_port,
            db_name=self.test_db_name,
        )


def get_settings():
    load_dotenv(".env")
    config_cls_dict = {
        DEVELOPMENT_ENVIRONMENT: DevelopmentConfig,
        UAT_ENVIRONMENT: UatConfig,
        PRODUCTION_ENVIRONMENT: ProductionConfig,
        TESTING_ENVIRONMENT: TestingConfig,
    }
    config_name = os.getenv("APP_ENV", default=DEVELOPMENT_ENVIRONMENT)
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()