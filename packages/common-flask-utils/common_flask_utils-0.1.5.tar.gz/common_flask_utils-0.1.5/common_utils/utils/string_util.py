import re


def to_lower_camel_case(s: str) -> str:
    """
    Converts a string to lower camel case.

    Args:
        s (str): The input string.

    Returns:
        str: The converted string in lower camel case.

    Examples:
        >>> to_lower_camel_case("hello_world")
        'helloWorld'
        >>> to_lower_camel_case("HELLO_WORLD")
        'helloWorld'
        >>> to_lower_camel_case("HelloWorld")
        'helloWorld'
        >>> to_lower_camel_case("hello-world")
        'helloWorld'
    """
    if re.search(r"(_|-)+", s):
        parts = re.split(r"_|-", s)
        return parts[0].lower() + "".join([part.title() for part in parts[1:]])
    if s.isupper():
        return s.lower()
    if re.search(r"[A-Z]", s):
        _s = re.sub(r"(?<!^)(?=[A-Z])", "_", s)
        parts = _s.split("_")
        return parts[0].lower() + "".join([part.title() for part in parts[1:]])
    return s


def to_upper_camel_case(s: str) -> str:
    """
    Converts a string to upper camel case.

    Args:
        s (str): The input string.

    Returns:
        str: The string converted to upper camel case.

    Example:
        >>> to_upper_camel_case("hello_world")
        'HelloWorld'
    """
    _s = to_lower_camel_case(s)
    if not _s:
        return ""
    return _s[0].upper() + _s[1:]


def to_lower_snake_case(s: str) -> str:
    """
    Converts a string to lower snake case.

    Args:
        s (str): The input string.

    Returns:
        str: The string converted to lower snake case.

    Example:
        >>> to_lower_snake_case("HelloWorld")
        'hello_world'
    """
    _s = to_upper_camel_case(s)
    _l = re.split(r"([A-Z][a-z0-9]+)", _s)
    return "_".join([part.lower() for part in _l if part]).strip("_")


def to_upper_snake_case(s: str) -> str:
    """
    Converts a string to upper snake case.

    Args:
        s (str): The input string.

    Returns:
        str: The string converted to upper snake case.
    """
    _s = to_lower_snake_case(s)
    return _s.upper()
