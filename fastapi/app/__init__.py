from logging.config import dictConfig

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi_pagination import add_pagination
from sqlalchemy.exc import DBAPIError

from app import api
from app.core.exceptions import AppExceptionCase, app_exception_handler
from app.core.extensions import celery
from app.core.log import log_config
from app.producer import KafkaPublisher
from app.services import RedisService
from config import settings


def create_app(**kwargs):
    dictConfig(log_config())
    app = FastAPI(
        title=settings.app_name,
        description="entry point for clients to submit resource requests.",
        version="1.0.0",
        docs_url="/resource",
        openapi_url="/resource/openapi.json",
    )
    register_api_routers(app)
    register_middlewares(app)
    register_extensions(app)
    register_event(app)
    return app


def register_api_routers(app: FastAPI):
    api.init_api_v1(app)

    @app.get("/", include_in_schema=False)
    def index():
        return RedirectResponse("/resource")

    return None


def register_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins.split("|"),
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return None


def register_extensions(app: FastAPI):
    add_pagination(app)

    @app.exception_handler(HTTPException)
    def handle_http_exception(request, exc):
        return app_exception_handler.http_exception_handler(exc)

    @app.exception_handler(DBAPIError)
    def handle_db_exception(request, exc):
        return app_exception_handler.db_exception_handler(exc)

    @app.exception_handler(AppExceptionCase)
    def handle_app_exceptions(request, exc):
        return app_exception_handler.app_exception_handler(exc)

    @app.exception_handler(RequestValidationError)
    def handle_validation_exceptions(request, exc):
        return app_exception_handler.validation_exception_handler(exc)

    return None


def register_event(app):
    @app.on_event("startup")
    async def startup():
        pass

    @app.on_event("shutdown")
    async def shutdown():
        KafkaPublisher.close()

    return None


def init_celery():
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
