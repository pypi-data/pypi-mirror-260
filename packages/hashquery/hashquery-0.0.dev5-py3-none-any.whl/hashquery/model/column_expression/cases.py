from typing import *

from ...utils.builder import builder_method
from ...utils.keypath.resolve import defer_keypath_args
from .column_expression import ColumnExpression
from .py_value import PyValueColumnExpression


@defer_keypath_args
def cases(
    *cases: Tuple["ColumnExpression", Union["ColumnExpression", Any]],
    other: Optional[Union["ColumnExpression", Any]] = None,
) -> "ColumnExpression":
    """
    Constructs a ColumnExpression that represents a SQL `CASE` expression.

    Args:
        *cases: List of (condition, value) pairs, where `condition` and `value` are ColumnExpressions.
        other: The value (or expression) to use if none of the cases match. Defaults to None.
    """
    # Coerce everything into expressions.
    coerced_cases = []
    for condition, value in list(cases):
        if not isinstance(condition, ColumnExpression):
            condition = PyValueColumnExpression(condition)
        if not isinstance(value, ColumnExpression):
            value = PyValueColumnExpression(value)
        coerced_cases.append((condition, value))
    if not isinstance(other, ColumnExpression):
        other = PyValueColumnExpression(other)

    return CasesColumnExpression(
        coerced_cases,
        other=other,
    )


class CasesColumnExpression(ColumnExpression):
    def __init__(
        self,
        cases: List[Tuple[ColumnExpression, ColumnExpression]],
        other: ColumnExpression,
    ) -> None:
        super().__init__()
        self.cases = cases
        self.other = other

    def default_identifier(self) -> Optional[str]:
        # consumers need to name this.
        return None

    @builder_method
    def disambiguated(self, namespace) -> "ColumnExpression":
        for c, v in self.cases:
            c.disambiguated(namespace)
            v.disambiguated(namespace)
        self.other.disambiguated(namespace)

    def __repr__(self) -> str:
        return f"CASE"

    # --- Serialization ---

    __TYPE_KEY__ = "case"

    def to_wire_format(self) -> dict:
        return {
            **super().to_wire_format(),
            "cases": [[c.to_wire_format(), v.to_wire_format()] for c, v in self.cases],
            "other": self.other.to_wire_format(),
        }

    @classmethod
    def from_wire_format(cls, wire: dict) -> "CasesColumnExpression":
        assert wire["subType"] == cls.__TYPE_KEY__
        return CasesColumnExpression(
            [
                (
                    ColumnExpression.from_wire_format(c),
                    ColumnExpression.from_wire_format(v),
                )
                for c, v in wire["cases"]
            ],
            ColumnExpression.from_wire_format(wire["other"]),
        )._from_wire_format_shared(wire)
