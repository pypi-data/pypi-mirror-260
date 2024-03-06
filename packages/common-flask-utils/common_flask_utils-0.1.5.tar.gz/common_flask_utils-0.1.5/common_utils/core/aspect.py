from functools import wraps
from typing import List

from flask import request
from .mapper import User

from .unify_exception import Forbidden


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            raise Forbidden()
        try:
            User.parse_token(token)
        except Exception as e:
            raise e
        return f(*args, **kwargs)

    return decorated
