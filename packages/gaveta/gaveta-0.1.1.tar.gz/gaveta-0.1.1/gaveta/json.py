import json
from enum import Enum
from pathlib import Path
from typing import TypeAlias

from gaveta.utils import assert_never

# Source:
# - Great Expectations (https://github.com/great-expectations/great_expectations/blob/0.18.10/great_expectations/alias_types.py)
# - Shantanu (https://github.com/python/typing/issues/182#issuecomment-1320974824)
JSONValues: TypeAlias = (
    dict[str, "JSONValues"] | list["JSONValues"] | str | int | float | bool | None
)


class EOF(Enum):
    NL = 1
    DEFAULT = 2


def write_json(
    data: JSONValues, output_path: Path, indent: int = 2, eof: EOF = EOF.NL
) -> None:
    with output_path.open(mode="w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)

        match eof:
            case EOF.NL:
                f.write("\n")
            case EOF.DEFAULT:
                pass
            case _:
                assert_never(eof)
