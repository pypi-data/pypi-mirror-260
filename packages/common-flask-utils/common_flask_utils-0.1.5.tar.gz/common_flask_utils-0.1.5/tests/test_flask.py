from common_utils.core.scaffold import Flask


app = Flask(__name__)


class TestFlask:
    def setup_method(self):
        self.client = app.test_client()

    def test_urls(self):
        response = self.client.get("/urls")
        ret = response.get_json()
        assert ret.get("code") == 20000
        assert len(ret.get("data")) == 2
        assert ret.get("message") == "成功"
