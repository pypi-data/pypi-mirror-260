from common_utils.core.unify_exception import (
    BadRequest,
    DataNotFound,
    Forbidden,
    I18nNotFound,
    InternalServerError,
    MethodNotAllowed,
    NotFound,
    TokenExpired,
    Unauthorized,
)


def test_bad_request():
    # Test default values
    exception = BadRequest()
    assert exception.code == 40000
    assert exception.message == "失败"

    # Test custom values
    exception = BadRequest(code=40002, message="Custom Bad Request")
    assert exception.code == 40002
    assert exception.message == "Custom Bad Request"


def test_unauthorized():
    # Test default values
    exception = Unauthorized()
    assert exception.code == 40101
    assert exception.message == "未授权"

    # Test custom values
    exception = Unauthorized(code=40102, message="Custom Unauthorized")
    assert exception.code == 40102
    assert exception.message == "Custom Unauthorized"


def test_forbidden():
    # Test default values
    exception = Forbidden()
    assert exception.code == 40301
    assert exception.message == "禁止"

    # Test custom values
    exception = Forbidden(code=40302, message="Custom Forbidden")
    assert exception.code == 40302
    assert exception.message == "Custom Forbidden"


def test_token_invalid_or_expired():
    # Test default values
    exception = TokenExpired()
    assert exception.code == 40303
    assert exception.message == "Token Expired"

    # Test custom values
    exception = TokenExpired(code=40303, message="Custom Token Invalid Or Expired")
    assert exception.code == 40303
    assert exception.message == "Custom Token Invalid Or Expired"


def test_not_found():
    # Test default values
    exception = NotFound()
    assert exception.code == 40400
    assert exception.message == "未找到"

    # Test custom values
    exception = NotFound(code=40401, message="Custom Not Found")
    assert exception.code == 40401
    assert exception.message == "Custom Not Found"


def test_i18n_not_found():
    # Test default values
    exception = I18nNotFound()
    assert exception.code == 40402
    assert exception.message == "I18n 未找到"

    # Test custom values
    exception = I18nNotFound(code=40403, message="Custom I18n Not Found")
    assert exception.code == 40403
    assert exception.message == "Custom I18n Not Found"


def test_method_not_allowed():
    # Test default values
    exception = MethodNotAllowed()
    assert exception.code == 40500
    assert exception.message == "Method Not Allowed"

    # Test custom values
    exception = MethodNotAllowed(code=40501, message="Custom Method Not Allowed")
    assert exception.code == 40501
    assert exception.message == "Custom Method Not Allowed"


def test_internal_server_error():
    # Test default values
    exception = InternalServerError()
    assert exception.code == 50000
    assert exception.message == "内部服务器错误"

    # Test custom values
    exception = InternalServerError(code=50001, message="Custom Internal Server Error")
    assert exception.code == 50001
    assert exception.message == "Custom Internal Server Error"


def test_data_not_found():
    # Test default values
    exception = DataNotFound()
    assert exception.code == 50001
    assert exception.message == "数据库错误"

    # Test custom values
    exception = DataNotFound(code=50002, message="Custom Data Not Found")
    assert exception.code == 50002
    assert exception.message == "Custom Data Not Found"
