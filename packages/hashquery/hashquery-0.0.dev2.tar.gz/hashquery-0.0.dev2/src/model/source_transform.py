from typing import *

from .source import Source
from .column_expression import ColumnExpression
from .relation import ModelRelation


class TransformedSource(Source):
    def __init__(self, base: Source) -> None:
        super().__init__()
        self.base = base

    def to_wire_format(self) -> dict:
        return {
            "type": "source",
            "subType": "transform",
            "base": self.base.to_wire_format(),
            "transformType": "<ABSTRACT_BASE>",
        }

    @classmethod
    def from_wire_format(cls, wire: dict):
        assert wire["type"] == "source" and wire["subType"] == "transform"
        base = Source.from_wire_format(wire["base"])
        if wire["transformType"] == "aggregate":
            return AggregateSource.from_wire_format(base, wire)
        elif wire["transformType"] == "filter":
            return FilterSource.from_wire_format(base, wire)
        elif wire["transformType"] == "sort":
            return SortSource.from_wire_format(base, wire)
        elif wire["transformType"] == "limit":
            return LimitSource.from_wire_format(base, wire)
        elif wire["transformType"] == "select":
            return SelectSource.from_wire_format(base, wire)
        elif wire["transformType"] == "joinOne":
            return JoinOneSource.from_wire_format(base, wire)
        else:
            raise AssertionError(
                "Unknown Source transformType: " + wire["transformType"]
            )


class AggregateSource(TransformedSource):
    def __init__(
        self,
        base: Source,
        *,
        groups: List[ColumnExpression],
        measures: List[ColumnExpression],
    ) -> None:
        super().__init__(base)
        self.groups = groups
        self.measures = measures

    def __repr__(self) -> str:
        return (
            str(self.base)
            + "\n -> AGGREGATE "
            + f"MEASURES {','.join(str(m) for m in self.measures)} "
            + f"BY {','.join(str(g) for g in self.groups)}"
        )

    def to_wire_format(self) -> dict:
        return {
            **super().to_wire_format(),
            "transformType": "aggregate",
            "groups": [g.to_wire_format() for g in self.groups],
            "measures": [m.to_wire_format() for m in self.measures],
        }

    @classmethod
    def from_wire_format(cls, base: Source, wire: dict):
        assert wire["transformType"] == "aggregate"
        return AggregateSource(
            base,
            groups=[ColumnExpression.from_wire_format(g) for g in wire["groups"]],
            measures=[ColumnExpression.from_wire_format(m) for m in wire["measures"]],
        )


class FilterSource(TransformedSource):
    def __init__(self, base: Source, condition: ColumnExpression) -> None:
        super().__init__(base)
        self.condition = condition

    def __repr__(self) -> str:
        return str(self.base) + f"\n -> FILTER {str(self.condition)}"

    def to_wire_format(self) -> dict:
        return {
            **super().to_wire_format(),
            "transformType": "filter",
            "condition": self.condition.to_wire_format(),
        }

    @classmethod
    def from_wire_format(cls, base: Source, wire: dict):
        assert wire["transformType"] == "filter"
        return FilterSource(base, ColumnExpression.from_wire_format(wire["condition"]))


class SortSource(TransformedSource):
    def __init__(self, base: Source, sort: ColumnExpression) -> None:
        super().__init__(base)
        self.sort = sort

    def __repr__(self) -> str:
        return str(self.base) + f"\n -> ORDER BY {str(self.sort)}"

    def to_wire_format(self) -> dict:
        return {
            **super().to_wire_format(),
            "transformType": "sort",
            "sort": self.sort.to_wire_format(),
        }

    @classmethod
    def from_wire_format(cls, base: Source, wire: dict):
        assert wire["transformType"] == "sort"
        return SortSource(base, ColumnExpression.from_wire_format(wire["sort"]))


class LimitSource(TransformedSource):
    def __init__(self, base: Source, limit: int) -> None:
        super().__init__(base)
        self.limit = limit

    def __repr__(self) -> str:
        return str(self.base) + f"\n -> LIMIT {self.limit}"

    def to_wire_format(self) -> dict:
        return {
            **super().to_wire_format(),
            "transformType": "limit",
            "limit": self.limit,
        }

    @classmethod
    def from_wire_format(cls, base: Source, wire: dict):
        assert wire["transformType"] == "limit"
        return LimitSource(base, wire["limit"])


class SelectSource(TransformedSource):
    def __init__(self, base: Source, selections: List[ColumnExpression]) -> None:
        super().__init__(base)
        self.selections = selections

    def __repr__(self) -> str:
        return (
            str(self.base) + "\n -> SELECT " + ",".join(str(m) for m in self.selections)
        )

    def to_wire_format(self) -> dict:
        return {
            **super().to_wire_format(),
            "transformType": "select",
            "selections": [s.to_wire_format() for s in self.selections],
        }

    @classmethod
    def from_wire_format(cls, base: Source, wire: dict):
        assert wire["transformType"] == "select"
        return SelectSource(
            base,
            [ColumnExpression.from_wire_format(s) for s in wire["selections"]],
        )


class JoinOneSource(TransformedSource):
    def __init__(self, base: Source, relation: ModelRelation) -> None:
        super().__init__(base)
        self.relation = relation

    def __repr__(self) -> str:
        return str(self.base) + f"\n -> JOIN ONE {self.relation}"

    def to_wire_format(self) -> dict:
        return {
            **super().to_wire_format(),
            "transformType": "joinOne",
            "relation": self.relation.to_wire_format(),
        }

    @classmethod
    def from_wire_format(cls, base: Source, wire: dict):
        assert wire["transformType"] == "joinOne"
        return JoinOneSource(
            base,
            ModelRelation.from_wire_format(wire["relation"]),
        )
