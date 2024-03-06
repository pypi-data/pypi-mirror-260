from os.path import exists, join
from typing import Dict, List

from flask import Flask

default_config: Dict[str, str] = {
    "HOST": "0.0.0.0",
    "PORT": 5000,
    "DEBUG": True,
    "SQLALCHEMY_DATABASE_URI": "sqlite:///tests/test.sqlite3", # in memory sqlite://:memory:
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    "SQLALCHEMY_ECHO": True,
    "JWT_SECRET_KEY": "secret",
    "JWT_EXPIRATION": 60 * 60 * 24 * 7,  # 1 week
    "JWT_ALGORITHM": "HS256",
    "JWT_PREFIX": "Bearer"
}


def flask_config_registration(
    app: Flask, config_dir: dir = None, configs: List[str] = None
) -> None:
    app.config.update(default_config)

    if config_dir is None:
        return
    for config in configs:
        config_path: str = join(config_dir, f"{config}.py")
        if not exists(config_path):
            continue
        app.config.from_pyfile(config_path)
