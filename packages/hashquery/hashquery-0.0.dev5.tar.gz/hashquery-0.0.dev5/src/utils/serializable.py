from typing import *
from typing_extensions import Self
from datetime import date, datetime

WireFormat = TypeVar("WireFormat")


class Serializable(Protocol[WireFormat]):
    def to_wire_format(self) -> WireFormat:
        ...

    @classmethod
    def from_wire_format(cls, wire: WireFormat) -> Self:
        ...

    @classmethod
    def _primitive_to_wire_format(cls, value):
        if isinstance(value, datetime):
            return {"$typeKey": "py.datetime", "iso": value.isoformat()}
        elif isinstance(value, date):
            return {"$typeKey": "py.date", "iso": value.isoformat()}
        # directly serializable to JSON without type information
        return value

    @classmethod
    def _primitive_from_wire_format(cls, wire):
        type_key = wire.get("$typeKey") if type(wire) == dict else None
        if not type_key:
            return wire
        elif type_key == "py.datetime":
            return datetime.fromisoformat(wire["iso"])
        elif type_key == "py.date":
            return date.fromisoformat(wire["iso"])
        else:
            raise ValueError(
                "Cannot deserialize value. `$typeKey` is present but an unrecognized type. "
                + wire
            )
