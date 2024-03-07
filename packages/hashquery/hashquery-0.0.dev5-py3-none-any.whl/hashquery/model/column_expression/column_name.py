from typing import *

from .column_expression import ColumnExpression
from ..relation import ModelRelation
from ...utils.builder import builder_method


def column(sql: str) -> "ColumnNameColumnExpression":
    """
    Constructs a ColumnExpression with the provided column name
    as its contents. This name will be escaped according to the
    database dialect, and always be correctly scoped.
    """
    return ColumnNameColumnExpression(sql)


class ColumnNameColumnExpression(ColumnExpression):
    def __init__(self, column_name: str) -> None:
        super().__init__()
        self.column_name = column_name
        self._namespace_identifier: Optional[str] = None

    def default_identifier(self) -> str:
        if self.column_name.isidentifier():
            return self.column_name
        return None

    @builder_method
    def disambiguated(self, namespace) -> "ColumnNameColumnExpression":
        self._namespace_identifier = (
            namespace.identifier if type(namespace) == ModelRelation else namespace
        )

    def __repr__(self) -> str:
        return f"`{self.column_name}`"

    # --- Serialization ---

    __TYPE_KEY__ = "columnName"

    def to_wire_format(self) -> dict:
        return {
            **super().to_wire_format(),
            "columnName": self.column_name,
            "namespaceIdentifier": self._namespace_identifier,
        }

    @classmethod
    def from_wire_format(cls, wire: dict) -> "ColumnNameColumnExpression":
        assert wire["subType"] == cls.__TYPE_KEY__
        result = ColumnNameColumnExpression(wire["columnName"])
        result._namespace_identifier = wire["namespaceIdentifier"]
        result._from_wire_format_shared(wire)
        return result
