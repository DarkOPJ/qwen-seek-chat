from typing import Any

from fastapi import status
from fastapi.logger import logger


class AppExceptionCase(Exception):
    """
    base exception to be raised by the application
    """

    def __init__(self, status_code: int, error_message: Any, context=None):
        self.exception_case = self.__class__.__name__
        self.status_code = status_code
        self.error_message = error_message
        self.context = context
        if self.error_message:
            logger.error(self.error_message)
        else:
            logger.critical(self.context)

    def __str__(self):
        return (
            f"<AppException {self.exception_case} - "
            + f"status_code = {self.status_code} - error_message = {self.error_message}>"
        )


class AppException:
    """
    the various exceptions that will be raised by the application
    """

    class BadRequestException(AppExceptionCase):
        """
        exception to catch errors caused by invalid requests
        :param error_message: the message return from request
        :param context: other message suitable for troubleshooting errors
        """

        def __init__(self, error_message, context=None):
            super().__init__(status.HTTP_400_BAD_REQUEST, error_message, context)

    class InternalServerException(AppExceptionCase):
        """
        exception to catch errors caused by servers inability to process an operation
        :param error_message: the message return from request
        :param context: other message suitable for troubleshooting errors
        """

        def __init__(self, error_message, context=None):
            super().__init__(
                status.HTTP_500_INTERNAL_SERVER_ERROR, error_message, context
            )

    class ResourceExistException(AppExceptionCase):
        """
        exception to catch errors caused by resource duplication
        :param error_message: the message return from request
        :param context: other message suitable for troubleshooting errors
        """

        def __init__(self, error_message, context=None):
            super().__init__(status.HTTP_409_CONFLICT, error_message, context)

    class NotFoundException(AppExceptionCase):
        """
        exception to catch errors caused by resource nonexistence
        :param error_message: the message return from request
        :param context: other message suitable for troubleshooting errors
        """

        def __init__(self, error_message, context=None):
            super().__init__(status.HTTP_404_NOT_FOUND, error_message, context)

    class UnauthorizedException(AppExceptionCase):
        """
        exception to catch errors caused by illegitimate operation
        :param error_message: the message return from request
        :param context: other message suitable for troubleshooting errors
        """

        def __init__(self, error_message, context=None):
            super().__init__(status.HTTP_401_UNAUTHORIZED, error_message, context)

    class PermissionException(AppExceptionCase):
        """
        exception to catch errors caused by illegitimate operation
        :param error_message: the message return from request
        :param context: other message suitable for troubleshooting errors
        """

        def __init__(self, error_message, context=None):
            super().__init__(status.HTTP_403_FORBIDDEN, error_message, context)

    class ValidationException(AppExceptionCase):
        """
        exception the catch errors caused by invalid data
        :param error_message: the message return from request
        :param context: other message suitable for troubleshooting errors
        """

        def __init__(self, error_message, context=None):
            super().__init__(
                status.HTTP_422_UNPROCESSABLE_ENTITY, error_message, context
            )
