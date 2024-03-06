import datetime
import decimal
import json
import logging
from math import ceil
from typing import Any

from flask import Flask as _Flask
from flask import Response, request
from flask.json.provider import DefaultJSONProvider
from flask_cors import CORS

from ..types.flask_type import IFlaskResponseRV
from ..utils.blueprint_util import blueprint_registration
from ..utils.config_util import flask_config_registration
from ..utils.logger_util import logger_registration
from .mapper import db
from .unify_exception import IException
from .unify_response import IResult, R

logger: logging.Logger = logging.getLogger("Flask")


class JSONProvider(DefaultJSONProvider):
    """A custom JSON provider that extends the DefaultJSONProvider class."""

    def dumps(self, o: Any, **kwargs: Any) -> str:
        """
        Serialize an object to a JSON formatted string.

        Args:
            o (Any): The object to be serialized.
            **kwargs (Any): Additional keyword arguments to be passed to the json.dumps() function.

        Returns:
            str: The JSON formatted string representation of the object.
        """
        if hasattr(o, "keys") and hasattr(o, "__getitem__"):
            o = dict(o)

        if isinstance(o, datetime.date):
            o = o.strftime("%Y-%m-%d")

        if isinstance(o, decimal.Decimal):
            o = float(o)

        if isinstance(o, bytes):
            o = o.decode("utf-8")

        return json.dumps(o, **kwargs)


class Flask(_Flask):
    """
    Customized Flask class with additional error handlers and response handling.

    Inherits from the _Flask class and adds error handlers for 404, 405, and 500 errors.
    It also provides a custom implementation of the `make_response` method.

    Attributes:
        json_provider_class (class): The JSONProvider class used for JSON serialization.

    Methods:
        __init__: Initializes the Flask object and sets up the error handlers.
        make_response: Overrides the default `make_response` method to handle custom response objects.

    """

    json_provider_class = JSONProvider

    def __init__(self, *args, **kwargs):
        controller_scan_dir: str = kwargs.pop("controller_scan_dir", None)
        super().__init__(*args, **kwargs)

        flask_config_registration(self)
        logger_registration()

        if controller_scan_dir is not None:
            blueprint_registration(self, controller_scan_dir)

        self.default_error_handlers_registration()
        self.urls_route_registration()
        CORS(self)
        db.init_app(self)

    def urls_route_registration(self):
        if not self.config.get("DEBUG"):
            return

        @self.get("/urls")
        def urls():
            return [rule.rule for rule in self.url_map.iter_rules()]

    def default_error_handlers_registration(self):
        @self.errorhandler(404)
        def not_found(e):
            return R.fail(code=40400)

        @self.errorhandler(405)
        def not_allowed(e):
            return R.fail(code=40500)

        @self.errorhandler(500)
        def internal_server_error(e):
            return R.error()

        @self.errorhandler(Exception)
        def handle_exception(e):
            logger.exception(e)
            if isinstance(e, IException):
                return e.get_body()
            return R.error(message=str(e))

    def make_response(self, rv: IFlaskResponseRV) -> Response:
        """
        Custom implementation of the `make_response` method.

        This method is responsible for creating a Flask response object based on the provided return value (rv).
        If the return value is an instance of IResult, it is used as is.
        Otherwise, a default success response object is created and the return value is set as the data attribute.

        Args:
            rv (IFlaskResponseRV): The return value to be converted into a Flask response.

        Returns:
            Response: The Flask response object.

        """
        if isinstance(rv, IResult):
            ret = rv
        else:
            ret = R.success()
            ret.data = rv

        ret.path = request.path
        ret.method = request.method
        _code: str = getattr(rv, "code", 20000)
        status: int = ceil(_code / 100)
        return super().make_response((dict(ret), status))
