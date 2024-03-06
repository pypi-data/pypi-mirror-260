from common_utils.core.unify_response import R


def test_instance():
    # Test with integer signature
    result = R.instance(20000)
    assert result.code == 20000
    assert result.message == "成功"
    assert result.data is None

    # Test with dictionary signature
    result = R.instance({"code": 40000, "message": "Error"})
    assert result.code == 40000
    assert result.message == "Error"
    assert result.data is None

    # Test with invalid signature
    try:
        R.instance("invalid")
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError to be raised"


def test_success():
    # Test with default values
    result = R.success()
    assert result.code == 20000
    assert result.message == "成功"
    assert result.data is None

    # Test with custom values
    result = R.success(code=20001, message="Custom Success", data={"key": "value"})
    assert result.code == 20001
    assert result.message == "Custom Success"
    assert result.data == {"key": "value"}


def test_fail():
    # Test with default values
    result = R.fail()
    assert result.code == 40000
    assert result.message == "失败"
    assert result.data is None

    # Test with custom values
    result = R.fail(code=40001, message="Custom Error", data={"key": "value"})
    assert result.code == 40001
    assert result.message == "Custom Error"
    assert result.data == {"key": "value"}
