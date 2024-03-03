from typing import Any, NamedTuple, Optional

from nagiosplugin.context import Context
from nagiosplugin.performance import Performance
from nagiosplugin.resource import Resource
from nagiosplugin.result import Result
from typing_extensions import TypedDict, Unpack

class MetricKwargs(TypedDict, total=False):
    name: str
    value: Any
    uom: str
    min: float
    max: float
    context: str
    contextobj: Context
    resource: Resource

class Metric(
    NamedTuple(
        "Metric",
        [
            ("name", str),
            ("value", Any),
            ("uom", str),
            ("min", float),
            ("max", float),
            ("context", str),
            ("contextobj", Context),
            ("resource", Resource),
        ],
    )
):
    def __new__(
        cls,
        name: str,
        value: Any,
        uom: Optional[str] = ...,
        min: Optional[float] = ...,
        max: Optional[float] = ...,
        context: Optional[str] = ...,
        contextobj: Optional[Context] = ...,
        resource: Optional[Resource] = ...,
    ) -> Metric: ...
    def replace(self, **attr: Unpack[MetricKwargs]) -> Metric: ...
    @property
    def description(self) -> str: ...
    @property
    def valueunit(self) -> str: ...
    def evaluate(self) -> Result: ...
    def performance(self) -> Performance: ...
