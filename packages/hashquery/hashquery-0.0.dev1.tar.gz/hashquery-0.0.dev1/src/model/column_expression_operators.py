from typing import *

from .column_expression import ColumnExpression
from ..utils.builder import builder_method


class BinaryOpColumnExpression(ColumnExpression):
    def __init__(
        self,
        left: ColumnExpression,
        right: ColumnExpression,
        op: str,
    ) -> None:
        super().__init__()
        self.left = left
        self.right = right
        self.op = op

    def __repr__(self) -> str:
        return f"{self.left} {self.op} {self.right}"

    @builder_method
    def disambiguated(self, namespace) -> "BinaryOpColumnExpression":
        self.left.disambiguated(namespace)
        self.right.disambiguated(namespace)

    def to_wire_format(self) -> Any:
        return {
            **super().to_wire_format(),
            "subType": "binaryOp",
            "left": self.left.to_wire_format(),
            "right": self.right.to_wire_format(),
            "op": self.op,
        }

    def default_identifier(self) -> Optional[str]:
        return None

    @classmethod
    def from_wire_format(cls, wire: dict) -> "BinaryOpColumnExpression":
        assert wire["subType"] == "binaryOp"
        left = ColumnExpression.from_wire_format(wire["left"])
        right = ColumnExpression.from_wire_format(wire["right"])
        return BinaryOpColumnExpression(left, right, wire["op"])
