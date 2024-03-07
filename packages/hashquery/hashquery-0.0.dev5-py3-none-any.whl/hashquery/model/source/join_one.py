from typing import *

from .source import Source
from ..relation import ModelRelation


class JoinOneSource(Source):
    def __init__(self, base: Source, relation: ModelRelation) -> None:
        self.base = base
        self.relation = relation

    def __repr__(self) -> str:
        return str(self.base) + f"\n -> JOIN ONE {self.relation}"

    __TYPE_KEY__ = "joinOne"

    def to_wire_format(self) -> dict:
        return {
            **super().to_wire_format(),
            "base": self.base.to_wire_format(),
            "relation": self.relation.to_wire_format(),
        }

    @classmethod
    def from_wire_format(cls, wire: dict):
        assert wire["subType"] == cls.__TYPE_KEY__
        return JoinOneSource(
            Source.from_wire_format(wire["base"]),
            ModelRelation.from_wire_format(wire["relation"]),
        )
