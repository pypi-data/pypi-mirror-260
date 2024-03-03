from dataclasses import dataclass
from typing import Any, Literal

from .range import Range

def zap_none(val: Any | None) -> Any | Literal[""]: ...
def quote(label: str) -> str: ...
@dataclass
class Performance:
    label: str
    value: Any
    uom: str | None = None
    warn: Range | None = None
    crit: Range | None = None
    min: float | None = None
    max: float | None = None

    def __str__(self) -> str: ...
