from typing import Any, Literal, NamedTuple, Optional

from .range import RangOrString

def zap_none(val: Any | None) -> Any | Literal[""]: ...
def quote(label: str) -> str: ...

class Performance(
    NamedTuple(
        "Performance",
        [
            ("label", str),
            ("value", Any),
            ("uom", str),
            ("warn", RangOrString),
            ("crit", RangOrString),
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
        warn: Optional[RangOrString] = ...,
        crit: Optional[RangOrString] = ...,
        min: Optional[float] = ...,
        max: Optional[float] = ...,
    ) -> Performance: ...
