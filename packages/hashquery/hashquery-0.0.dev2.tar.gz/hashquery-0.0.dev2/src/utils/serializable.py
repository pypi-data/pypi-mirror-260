from typing import *
from typing_extensions import Self

WireFormat = TypeVar("WireFormat")


class Serializable(Protocol[WireFormat]):
    def to_wire_format(self) -> WireFormat:
        pass

    @classmethod
    def from_wire_format(cls, wire: WireFormat) -> Self:
        pass
