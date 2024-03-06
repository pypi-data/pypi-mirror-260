from common_utils.utils.string_util import to_lower_camel_case, to_lower_snake_case, to_upper_camel_case, to_upper_snake_case


def test_to_lower_camel_case():
    test_cases = [
        ("hello_world", "helloWorld"),
        ("hello-world", "helloWorld"),
        ("hello__world", "helloWorld"),
        ("HelloWorld", "helloWorld"),
        ("helloWorld", "helloWorld"),
        ("HELLO_WORLD", "helloWorld"),
        ("hello", "hello"),
        ("WORLD", "world"),
        ("", ""),
        ("123", "123"),
    ]

    for input_str, expected_output in test_cases:
        assert (
            to_lower_camel_case(input_str) == expected_output
        ), f"@@@@@ {input_str} -> {expected_output}"


def test_to_upper_camel_case():
    test_cases = [
        ("hello_world", "HelloWorld"),
        ("hello-world", "HelloWorld"),
        ("hello__world", "HelloWorld"),
        ("HelloWorld", "HelloWorld"),
        ("helloWorld", "HelloWorld"),
        ("HELLO_WORLD", "HelloWorld"),
        ("hello", "Hello"),
        ("WORLD", "World"),
        ("", ""),
        ("123", "123"),
    ]

    for input_str, expected_output in test_cases:
        assert (
            to_upper_camel_case(input_str) == expected_output
        ), f"@@@@@ {input_str} -> {expected_output}"


def test_to_lower_snake_case():
    test_cases = [
        ("helloWorld", "hello_world"),
        ("HelloWorld", "hello_world"),
        ("HELLO_WORLD", "hello_world"),
        ("hello", "hello"),
        ("WORLD", "world"),
        ("", ""),
        ("123", "123"),
    ]

    for input_str, expected_output in test_cases:
        assert (
            to_lower_snake_case(input_str) == expected_output
        ), f"@@@@@ {input_str} -> {expected_output}"


def test_to_upper_snake_case():
    test_cases = [
        ("helloWorld", "HELLO_WORLD"),
        ("HelloWorld", "HELLO_WORLD"),
        ("HELLO_WORLD", "HELLO_WORLD"),
        ("hello", "HELLO"),
        ("WORLD", "WORLD"),
        ("", ""),
        ("123", "123"),
    ]

    for input_str, expected_output in test_cases:
        assert (
            to_upper_snake_case(input_str) == expected_output
        ), f"@@@@@ {input_str} -> {expected_output}"
