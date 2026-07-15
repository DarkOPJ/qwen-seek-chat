import logging
from datetime import datetime
from logging.handlers import SMTPHandler
from threading import Thread

from config import settings


def get_full_class_name(obj):
    module = obj.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return obj.__class__.__name__
    return module + "." + obj.__class__.__name__


def get_error_context(
    module, method, error, calling_method=None, calling_module=None, exc_class=None
):
    return {
        "exception_class": exc_class,
        "module": module,
        "method": method,
        "calling module": calling_module,
        "calling method": calling_method,
        "error": error,
    }


class MailHandler(SMTPHandler):
    def emit(self, record):
        """
        Emit a record.
        Format the record and send it to the specified addressees.
        """
        Thread(target=self.send_mail, kwargs={"record": record}).start()

    def send_mail(self, record):
        self.timeout = 30
        super().emit(record)


class RequestFormatter(logging.Formatter):
    def format(self, record):
        return super().format(record)


class MailHandlerFilter(logging.Filter):
    def __init__(self):
        super().__init__()

    def filter(self, record):
        log_message = record.getMessage()
        if log_message.startswith("[!ALERT]"):
            return True
        return False


def log_config():
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "loggers": {
            "root": {
                "level": "DEBUG",
                "handlers": [
                    "console_handler",
                    "error_file_handler",
                    "mail_handler",
                ],
            },
        },
        "handlers": {
            "console_handler": {
                "level": "ERROR",
                "class": "logging.StreamHandler",
                "formatter": "error_formatter",
                "stream": "ext://sys.stdout",
            },
            "mail_handler": {
                "()": "app.core.log.MailHandler",
                "formatter": "error_formatter",
                "level": "CRITICAL",
                "filters": ["limit_mail_logs"],
                "mailhost": (settings.mail_server, settings.mail_server_port),
                "fromaddr": f"{settings.default_mail_sender} <{settings.default_mail_sender_address}>",  # noqa
                "toaddrs": settings.maintainer_mail_address.split("|"),
                "subject": f"{settings.log_header}[{settings.app_env}_{datetime.utcnow().date()}]",  # noqa
                "credentials": (
                    settings.default_mail_sender_address,
                    settings.default_mail_sender_password,
                ),
                "secure": (),
            },
            "error_file_handler": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "formatter": "error_formatter",
                "level": "ERROR",
                "filename": f"{settings.app_root}/logs/error.log",
                "when": "D",
                "interval": 30,
                "backupCount": 1,
            },
            "access_file_handler": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "formatter": "access_formatter",
                "filename": f"{settings.app_root}/logs/access.log",
                "when": "D",
                "interval": 30,
                "backupCount": 1,
            },
        },
        "formatters": {
            "access_formatter": {
                "format": "%(message)s",
            },
            "error_formatter": {
                "()": "app.core.log.RequestFormatter",
                "format": """
                \n--- Logging %(levelname)s at %(asctime)s --- \n%(message)s
                """,
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "filters": {"limit_mail_logs": {"()": "app.core.log.MailHandlerFilter"}},
    }
