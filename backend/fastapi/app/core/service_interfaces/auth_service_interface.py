import abc


class AuthServiceInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "get_token")
            and callable(subclass.get_token)
            and hasattr(subclass, "refresh_token")
            and callable(subclass.refresh_token)
            and hasattr(subclass, "decode_token")
            and callable(subclass.decode_token)
        )

    @abc.abstractmethod
    def get_token(self, request_data: dict):
        """
        :param request_data: refresh token needed to get the next valid token
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def refresh_token(self, request_data: dict):
        """
        :param request_data: refresh token needed to get the next valid token
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def decode_token(self, token: str):
        """
        :param token: token to decode
        :return:
        """
        raise NotImplementedError
