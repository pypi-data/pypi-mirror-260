import json
from http.client import HTTPException
from math import ceil

from ..utils.i18n_util import t


class IException(HTTPException):
    code = 50000
    message = t("message.unknown")

    def __init__(self, code=None, message=None, headers=None) -> None:
        if code:
            self.code = code
            self.error_code = ceil(code / 100)
        if message:
            self.message = message

        super().__init__(self.message, headers)

    def get_body(self, environ=None):
        body = dict(message=self.message, code=self.code, error_code=self.error_code)
        return json.dumps(body)

    def get_headers(self, environ=None):
        return [("Content-Type", "application/json")]


class BadRequest(IException):
    code = 40000
    message = t(f"message.{code}", default="Bad Request")


class Unauthorized(IException):
    code = 40101
    message = t(f"message.{code}", default="Unauthorized")


class Forbidden(IException):
    code = 40301
    message = t(f"message.{code}", default="Forbidden")


class TokenInvalid(IException):
    code = 40302
    message = t(f"message.{code}", default="Token Invalid")


class TokenExpired(IException):
    code = 40303
    message = t(f"message.{code}", default="Token Expired")


class NotFound(IException):
    code = 40400
    message = t(f"message.{code}", default="Not Found")


class I18nNotFound(IException):
    code = 40402
    message = t(f"message.{code}", default="I18n Not Found")


class MethodNotAllowed(IException):
    code = 40500
    message = t(f"message.{code}", default="Method Not Allowed")


class InternalServerError(IException):
    code = 50000
    message = t(f"message.{code}", default="Internal Server Error")


class DataNotFound(IException):
    code = 50001
    message = t(f"message.{code}", default="Data Not Found")
