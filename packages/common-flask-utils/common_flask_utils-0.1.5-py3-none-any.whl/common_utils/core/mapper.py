# This module contains the `Entity` class, which is the base class for all mapper objects in the application.
import logging
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Literal, NotRequired, TypedDict

import jwt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from sqlalchemy import Column, String, orm
from werkzeug.security import check_password_hash, generate_password_hash

from ..utils.string_util import to_lower_camel_case
from .unify_exception import TokenExpired, TokenInvalid


class SQLAlchemy(_SQLAlchemy):
    def init_app(self, app: Flask) -> None:
        self.app = app
        return super().init_app(app)


db: SQLAlchemy = SQLAlchemy()

logger: logging.Logger = logging.getLogger("Mapper")


IMergeFieldsSettings = TypedDict(
    "IMergeFieldsSettings",
    {
        "use_low_camel_case": NotRequired[bool],
        "extra_fields": NotRequired[List[str]],
        "exclude_fields": NotRequired[List[str]],
        "only_fields": NotRequired[List[str]],
    },
)


class Entity(db.Model):
    __abstract__ = True
    cid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    createUserId = db.Column(
        db.Integer, nullable=False, name="create_user_id", default=-1
    )
    modifyUserId = db.Column(
        db.Integer, nullable=False, name="modify_user_id", default=-1
    )
    gmtCreate = db.Column(
        db.DateTime, nullable=False, name="gmt_create", default=db.func.now()
    )
    gmtModify = db.Column(
        db.DateTime,
        nullable=False,
        name="gmt_modify",
        default=db.func.now(),
        onupdate=db.func.now(),
    )
    status = db.Column(db.Integer, nullable=False, default=0)

    def __getitem__(self, item) -> any:
        """
        Retrieve the value of the specified attribute.

        Args:
            item (str): The name of the attribute to retrieve.

        Returns:
            any: The value of the specified attribute, or None if the attribute does not exist.
        """
        return getattr(self, item, None)

    def __init__(self, *args, **kwargs) -> None:
        self._init()
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        _items = [f"{k}={getattr(self, k)}" for k in self.keys()]
        return f"<{self.__class__.__name__}>({', '.join(_items)})"

    @orm.reconstructor
    def _init(self) -> None:
        self.app = db.app
        self._use_low_camel_case: bool = True
        self._extra_fields: List[str] = []  # extra fields for serialization
        self._exclude_fields: List[str] = [
            "createUserId",
            "modifyUserId",
            "gmtCreate",
            "gmtModify",
        ]  # exclude fields for serialization
        self._only_fields: List[str] = []  # only fields for serialization
        settings: IMergeFieldsSettings = self.merge_fields_settings()
        if settings is not None:
            use: bool = settings.pop("use_low_camel_case", True)
            if use is not None:
                self._use_low_camel_case = use
            for k, v in settings.items():
                field: str = f"_{k}"
                getattr(self, field, []).extend(v if isinstance(v, list) else [])

    @abstractmethod
    def merge_fields_settings(self) -> IMergeFieldsSettings:
        pass

    def keys(self):
        """
        Returns a list of keys representing the fields of the mapper object.

        If the `_only_fields` attribute is not empty, it returns the list of fields specified in `_only_fields`.
        Otherwise, it retrieves the keys from the `__table__.columns` attribute.
        If `use_low_camel_case` is True, the keys are converted to lower camel case using the `to_lower_camel_case` function.
        If `_exclude_fields` is a list and `_extra_fields` is not empty, the extra fields are added to the list of keys.
        Finally, it returns the list of keys excluding the fields specified in `_exclude_fields`.
        """
        if len(self._only_fields) > 0:
            return self._only_fields

        _items: List[str] = self.__table__.columns.keys()
        if self._use_low_camel_case:
            _items = [to_lower_camel_case(_) for _ in _items]

        if isinstance(self._exclude_fields, list) and len(self._extra_fields) > 0:
            _items.extend(self._extra_fields)

        return [item for item in _items if item not in self._exclude_fields]


class User(Entity):
    nickname = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=True)
    account = Column(String(255), nullable=False)
    _secret = Column(String(255), nullable=False, name="secret")
    email = Column(String(255), nullable=True)
    phone = Column(String(255), nullable=True)
    fax = Column(String(255), nullable=True)
    contact = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)

    @property
    def secret(self) -> str:
        return self._secret

    @secret.setter
    def secret(self, value: str) -> None:
        salted = f"{value}{self.account}"
        self._secret = generate_password_hash(salted, method="pbkdf2")

    def verify(self, password: str) -> bool:
        """
        Verifies if the provided password matches the hashed password stored in the object.

        Args:
            password (str): The password to be verified.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        salted = f"{password}{self.account}"
        return check_password_hash(self._secret, salted)

    def token(self, mapper: List[str] = None) -> str:
        """
        Generates a JSON Web Token (JWT) using the specified mapper.

        Args:
            mapper (List[str], optional): A list of attribute names to include in the token payload.
                If not provided, all attributes of the object will be included. Defaults to None.

        Returns:
            str: The generated JWT.

        """
        if mapper is None:
            mapper = self.keys()
        payload: Dict[str, Any] = {
            k: getattr(self, k) for k in mapper if hasattr(self, k)
        }

        payload["exp"] = self.calc_expiration()
        token = jwt.encode(
            payload,
            self.app.config.get("JWT_SECRET_KEY", ""),
            algorithm=self.app.config.get("JWT_ALGORITHM", "HS256"),
        )
        prefix: str = self.app.config.get("JWT_PREFIX", "Bearer")
        full_token: str = f"{prefix} {token}"
        logger.debug(f"token: {full_token}")
        return full_token

    def calc_expiration(self, expiration: int = None) -> int:
        """
        Calculate the expiration time as a Unix timestamp starting from the current time.

        Args:
            expiration (int, optional): The expiration time in seconds. If not provided, it will be fetched from the configuration key "JWT_EXPIRATION". Defaults to None.

        Returns:
            int: The calculated expiration time as a Unix timestamp.

        Notes:
            - The default expiration time is 1 week.
            - The expiration time unit is in seconds.
            - The expiration time in the configuration key is "JWT_EXPIRATION".
        """
        if expiration is None:
            expiration: int = self.app.config.get("JWT_EXPIRATION", 60 * 60 * 24 * 7)
        return int(expiration + time.time())

    def merge_fields_settings(self) -> IMergeFieldsSettings:
        return {"exclude_fields": ["secret"]}

    @staticmethod
    def parse_token(
        token: str, secret_key: str = None, algorithm: str = None, prefix: str = None
    ) -> Dict[str, Any]:
        """
        Parse a JSON Web Token (JWT) and return the decoded payload.

        Args:
            token (str): The JWT to be parsed.
            secret_key (str, optional): The secret key used to sign the JWT. If not provided, it will be retrieved from the app configuration.
            algorithm (str, optional): The algorithm used to sign the JWT. If not provided, it will be retrieved from the app configuration.
            prefix (str, optional): The prefix used to identify the JWT. If not provided, it will be retrieved from the app configuration.

        Returns:
            dict: The decoded payload of the JWT.

        Raises:
            TokenExpired: If the JWT has expired.
            TokenInvalid: If the JWT is invalid.
        """
        if secret_key is None:
            secret_key = db.app.config.get("JWT_SECRET_KEY", "")
        if algorithm is None:
            algorithm = db.app.config.get("JWT_ALGORITHM", "HS256")
        if prefix is None:
            prefix = db.app.config.get

        token = token.split(" ")[-1]
        try:
            return jwt.decode(token, secret_key, algorithms=[algorithm])
        except jwt.ExpiredSignatureError:
            raise TokenExpired()
        except jwt.InvalidTokenError:
            raise TokenInvalid()
