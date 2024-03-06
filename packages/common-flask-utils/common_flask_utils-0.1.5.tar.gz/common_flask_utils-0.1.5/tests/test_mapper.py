import pytest

from common_utils import Flask, db, User


class TestUser:
    def setup_method(self):
        self.app = Flask(__name__)
        self.client = self.app.test_client()

    def test_add_user(self):
        with self.app.app_context():
            user = User(nickname="test", account="test", secret="test")
            assert user is not None

    def test_user_token(self):
        with self.app.app_context():
            user = User(nickname="test", account="test", secret="test")
            token: str = user.token()
            assert token is not None

    def test_user_verify(self):
        with self.app.app_context():
            user = User(nickname="test", account="test", secret="test")
            assert user.verify("test")

    def test_user_parse_token(self):
        with self.app.app_context():
            user = User(nickname="test", account="test", secret="test")
            token: str = user.token()
            payload = user.parse_token(token)
            assert payload is not None
            assert payload.get("nickname") == "test"
