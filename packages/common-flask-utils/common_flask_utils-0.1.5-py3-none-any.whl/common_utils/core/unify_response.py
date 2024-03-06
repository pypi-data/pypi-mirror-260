from http import HTTPMethod
from typing import Generic, List, Optional, TypeVar, Union

from ..const.message import ELanguage
from ..utils.i18n_util import t

T = TypeVar("T")


class IResult(Generic[T]):
    def __init__(self, code: int, message: str, data: Optional[T] = None) -> None:
        """
        Initialize a new instance of the UnifyResponse class.

        Args:
            code (int): The response code.
            message (str): The response message.
            data (Optional[T], optional): The response data. Defaults to None.
        """
        self.code: int = code
        self.message: str = message
        self.data: Optional[T] = data
        self.method: HTTPMethod = "GET"
        self.path: str = "/"

    def __str__(self) -> str:
        """
        Returns a string representation of the object.

        The string representation includes the class name, base class name,
        code, message, and data of the object.

        Returns:
            str: The string representation of the object.
        """
        _t: str = "<{} | {}>(code={}, message={}, data={})"
        return _t.format(
            self.__class__.__name__,
            self.data.__class__.__name__ if self.data else "None",
            self.code,
            self.message,
            self.data,
        )

    def __getitem__(self, item: str) -> Optional[Union[int, str, T]]:
        """
        Retrieve the value of the specified attribute.

        Args:
            item (str): The name of the attribute to retrieve.

        Returns:
            Optional[Union[int, str, T]]: The value of the attribute, or None if it doesn't exist.
        """
        return getattr(self, item, None)

    def keys(self) -> List[str]:
        members: List[str] = ["code", "message", "data", "path", "method"]
        return list(filter(lambda x: hasattr(self, x), members))


class R:
    """
    A utility class for creating response objects.

    This class provides static methods for creating success and failure response objects.
    """

    _default_message: str = t("message.unknown")

    @staticmethod
    def instance(
        signature: Optional[Union[int, dict]] = None, _el: ELanguage = ELanguage.CHINESE
    ) -> IResult:
        """
        Create an instance of the IResult class based on the given signature.

        Args:
            signature (Optional[Union[int, dict]]): The signature to determine the code and message for the IResult instance.
                If an integer is provided, the corresponding message will be retrieved from RESPONSE_MESSAGE dictionary.
                If a dictionary is provided, it will be used to create the IResult instance directly.
            _el (ELanguage): The language to use for the message. Defaults to ELanguage.CHINESE.

        Returns:
            IResult: An instance of the IResult class.

        Raises:
            ValueError: If the signature is not an integer or a dictionary.
        """

        if isinstance(signature, int):
            message = t(f"message.{signature}", default=R._default_message)
            return IResult(code=signature, message=message)

        if isinstance(signature, dict):
            return IResult(**signature)
        raise ValueError("Invalid signature")

    @staticmethod
    def success(
        code: int = 20000,
        message: str = None,
        data: Optional[T] = None,
    ) -> IResult:
        """
        Create a success response.

        Args:
            code (int, optional): The response code. Defaults to 20000.
            message (str, optional): The response message. If not provided, a default message will be used based on the code. Defaults to None.
            data (Optional[T], optional): The response data. Defaults to None.

        Returns:
            IResult: The success response object.
        """

        if message is None:
            message = t(f"message.{code}", default=R._default_message)
        return IResult(code=code, message=message, data=data)

    @staticmethod
    def fail(
        code: int = 40000,
        message: str = None,
        data: Optional[T] = None,
    ) -> IResult:
        """
        Create a failure response.

        Args:
            code (int, optional): The error code. Defaults to 40000.
            message (str, optional): The error message. If not provided, a default message will be used based on the code. Defaults to None.
            data (Optional[T], optional): Additional data to include in the response. Defaults to None.

        Returns:
            IResult: The failure response object.
        """

        if message is None:
            message = t(f"message.{code}", default=R._default_message)
        return IResult(code=code, message=message, data=data)

    @staticmethod
    def error(
        code: int = 50000,
        message: str = None,
        data: Optional[T] = None,
    ) -> IResult:
        """
        Create an error response.

        Args:
            code (int): The error code.
            message (str, optional): The error message. If not provided, a default message will be used.
            data (Optional[T], optional): Additional data to include in the response.

        Returns:
            IResult: An instance of the IResult class representing the error response.
        """

        if message is None:
            message = t(f"message.{code}", default=R._default_message)
        return IResult(code=code, message=message, data=data)
