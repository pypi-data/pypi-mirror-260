from typing import *

from .source import Source


class LimitSource(Source):
    def __init__(self, base: Source, limit: int) -> None:
        self.base = base
        self.limit = limit

    def __repr__(self) -> str:
        return str(self.base) + f"\n -> LIMIT {self.limit}"

    __TYPE_KEY__ = "limit"

    def to_wire_format(self) -> dict:
        return {
            **super().to_wire_format(),
            "base": self.base.to_wire_format(),
            "limit": self.limit,
        }

    @classmethod
    def from_wire_format(cls, wire: dict):
        assert wire["subType"] == cls.__TYPE_KEY__
        return LimitSource(
            Source.from_wire_format(wire["base"]),
            wire["limit"],
        )
