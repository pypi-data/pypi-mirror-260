import logging
import os
import time
from io import TextIOWrapper
from logging.config import dictConfig
from logging.handlers import BaseRotatingHandler
from os import PathLike
from os.path import dirname
from typing import Dict

from .dict_util import merge


class SafeTimeRotatingFileHandler(BaseRotatingHandler):
    def __init__(
        self,
        filename: str | PathLike[str],
        encoding: str | None = None,
        delay: bool = False,
    ) -> None:
        self.suffix: str = "%Y-%m-%d"
        self.base_filename: str = filename
        self.current_file_name: str = self._compute_fn()
        if not os.path.exists(folder := dirname(filename)):
            os.makedirs(folder)
        super().__init__(filename, "a", encoding, delay)

    def shouldRollover(self, record: logging.LogRecord) -> bool:
        if self.current_file_name != self._compute_fn():
            return True
        return False

    def doRollover(self) -> None:
        if self.stream:
            self.stream.close()
            self.stream = None
        self.current_file_name = self._compute_fn()

    def _compute_fn(self) -> str:
        return f"{self.base_filename}.{time.strftime(self.suffix, time.localtime())}"

    def _open(self) -> TextIOWrapper:
        if self.encoding is None:
            stream = open(self.current_file_name, self.mode)
        else:
            stream = open(self.current_file_name, self.mode, encoding=self.encoding)

        if os.path.exists(self.base_filename):
            try:
                os.remove(self.base_filename)
            except OSError:
                pass
        try:
            os.symlink(self.current_file_name, self.base_filename)
        except OSError:
            pass

        return stream


_default_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s]-[%(levelname)8s] in %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "wsgi": {
            "class": "logging.StreamHandler",
            "level": logging.INFO,
            "formatter": "default",
            "stream": "ext://flask.logging.wsgi_errors_stream",
        },
        "file": {
            "class": "common_utils.utils.logger_util.SafeTimeRotatingFileHandler",
            "level": logging.INFO,
            "formatter": "default",
            "filename": "logs/app.log",
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "": {"level": logging.INFO, "handlers": ["wsgi", "file"]},
    },
}


def logger_registration(
    config: Dict = {}, formatter: Dict = {}, handlers: Dict = {}, loggers: Dict = {}
) -> None:
    options: Dict = merge(
        _default_config,
        config,
        {"formatters": formatter},
        {"handlers": handlers},
        {"loggers": loggers},
    )
    dictConfig(options)
