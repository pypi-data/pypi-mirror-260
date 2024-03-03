from typing import NamedTuple

def worst(states: list[ServiceState]) -> ServiceState: ...

class ServiceState(NamedTuple("ServiceState", [("code", int), ("text", str)])):
    def __int__(self) -> int: ...
    def __str__(self) -> str: ...

Ok: ServiceState
Warn: ServiceState
Critical: ServiceState
Unknown: ServiceState
