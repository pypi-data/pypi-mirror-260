from typing import *

from .column_expression import ColumnExpression
from ..utils.builder import builder_method


class TransformedColumnExpression(ColumnExpression):
    def __init__(self, base: ColumnExpression) -> None:
        super().__init__()
        self.base = base
        self._manually_set_identifier = base._manually_set_identifier

    def default_identifier(self) -> Optional[str]:
        return self.base.default_identifier()

    @builder_method
    def disambiguated(self, namespace) -> "TransformedColumnExpression":
        self.base.disambiguated(namespace)

    def to_wire_format(self) -> Any:
        return {
            **super().to_wire_format(),
            "subType": "transform",
            "base": self.base.to_wire_format(),
            "transformType": "<ABSTRACT_BASE>",
        }

    @classmethod
    def from_wire_format(cls, wire: dict) -> "TransformedColumnExpression":
        assert wire["subType"] == "transform"
        base = ColumnExpression.from_wire_format(wire["base"])
        if wire["transformType"] == "granularity":
            result = GranularityColumnExpression.from_wire_format(base, wire)
        else:
            raise AssertionError(
                "Unknown ColumnExpression transformType: " + wire["transformType"]
            )
        result._from_wire_format_shared(wire)
        return result


class GranularityColumnExpression(TransformedColumnExpression):
    def __init__(self, base: ColumnExpression, granularity: str) -> None:
        super().__init__(base)
        self.granularity = granularity

    def __repr__(self) -> str:
        return f'DATE_TRUNC({self.base}, "{self.granularity}")'

    def to_wire_format(self) -> dict:
        return {
            **super().to_wire_format(),
            "transformType": "granularity",
            "granularity": self.granularity,
        }

    @classmethod
    def from_wire_format(
        cls, base: ColumnExpression, wire: dict
    ) -> "GranularityColumnExpression":
        assert wire["transformType"] == "granularity"
        return GranularityColumnExpression(base, wire["granularity"])
