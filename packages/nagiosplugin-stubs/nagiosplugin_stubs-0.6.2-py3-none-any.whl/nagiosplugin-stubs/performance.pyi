from typing import Any, Literal, NamedTuple, Optional

from .range import Range

def zap_none(val: Any | None) -> Any | Literal[""]: ...
def quote(label: str) -> str: ...

class Performance(
    NamedTuple(
        "Performance",
        [
            ("label", str),
            ("value", Any),
            ("uom", str),
            ("warn", Range | str),
            ("crit", Range | str),
            ("min", float),
            ("max", float),
        ],
    )
):
    def __new__(
        cls,
        label: str,
        value: Any,
        uom: Optional[str] = ...,
        warn: Optional[Range | str] = ...,
        crit: Optional[Range | str] = ...,
        min: Optional[float] = ...,
        max: Optional[float] = ...,
    ) -> Performance: ...
