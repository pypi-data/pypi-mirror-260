from datetime import datetime, timezone
from enum import Enum

from gaveta.utils import assert_never


class ISOFormat(Enum):
    EXTENDED = 1
    BASIC = 2


def now_iso(iso_format: ISOFormat = ISOFormat.EXTENDED) -> str:
    dt = datetime.now(timezone.utc)

    match iso_format:
        case ISOFormat.EXTENDED:
            dt_iso = dt.isoformat(timespec="seconds").removesuffix("+00:00")
            return f"{dt_iso}Z"
        case ISOFormat.BASIC:
            return dt.strftime("%Y%m%dT%H%M%SZ")
        case _:
            assert_never(iso_format)
