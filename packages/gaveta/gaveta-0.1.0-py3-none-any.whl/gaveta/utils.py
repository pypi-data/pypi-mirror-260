from typing import NoReturn


def assert_never(value: NoReturn) -> NoReturn:
    msg = f"Unsupported value: {value} ({type(value).__name__})"
    raise AssertionError(msg)
