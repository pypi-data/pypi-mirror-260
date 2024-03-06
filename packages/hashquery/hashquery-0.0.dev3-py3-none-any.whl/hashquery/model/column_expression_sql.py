from typing import *

from .column_expression import ColumnExpression
from ..utils.builder import builder_method
from .relation import ModelRelation

# --- Public Exports ---


def column(sql: str) -> "ColumnNameColumnExpression":
    """
    Constructs a ColumnExpression with the provided column name
    as its contents. This name will be escaped according to the
    database dialect, and always be correctly scoped.
    """
    return ColumnNameColumnExpression(sql)


def value(value: Any) -> "PyValueColumnExpression":
    """
    Constructs a ColumnExpression which represents the given Python value.
    For example, `None` is translated to `NULL`.

    Generally you don't need to use this function explicitly; other functions
    are designed to automatically convert literal Python values into column
    expressions as needed.
    """
    return PyValueColumnExpression(value)


def sql(sql: str) -> "SqlTextColumnExpression":
    """
    Constructs a ColumnExpression from the provided literal SQL text.
    This SQL will be passed as is into the database without any escaping.
    """
    return SqlTextColumnExpression(sql)


# --- Structural Implementations ---


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

    def to_wire_format(self) -> dict:
        return {
            **super().to_wire_format(),
            "subType": "columnName",
            "columnName": self.column_name,
            "namespaceIdentifier": self._namespace_identifier,
        }

    @classmethod
    def from_wire_format(cls, wire: dict) -> "ColumnNameColumnExpression":
        assert wire["subType"] == "columnName"
        result = ColumnNameColumnExpression(wire["columnName"])
        result._namespace_identifier = wire["namespaceIdentifier"]
        result._from_wire_format_shared(wire)
        return result


class PyValueColumnExpression(ColumnExpression):
    def __init__(self, value: Any) -> None:
        super().__init__()
        self.value = value

    def default_identifier(self) -> Optional[str]:
        return None

    @builder_method
    def disambiguated(self, namespace) -> "PyValueColumnExpression":
        # a literal value never needs to be scoped/qualified
        pass

    def __repr__(self) -> str:
        if self.value is None:
            return "NULL"
        elif type(self.value) == str:
            return f"'{self.value}'"
        elif type(self.value) == bool:
            return str(self.value).upper()
        return str(self.value)

    def to_wire_format(self) -> dict:
        return {
            **super().to_wire_format(),
            "subType": "pyValue",
            "value": self.value,
        }

    @classmethod
    def from_wire_format(cls, wire: dict) -> "PyValueColumnExpression":
        assert wire["subType"] == "pyValue"
        result = PyValueColumnExpression(wire["value"])
        result._from_wire_format_shared(wire)
        return result


class SqlTextColumnExpression(ColumnExpression):
    def __init__(self, sql: str) -> None:
        super().__init__()
        self.sql = sql

    def default_identifier(self) -> str:
        if self.sql.isidentifier():
            return self.sql
        return None

    @builder_method
    def disambiguated(self, namespace) -> "SqlTextColumnExpression":
        # TODO: users need some ability to qualify their own textual
        # references in raw SQL; which right now they cannot
        pass

    def __repr__(self) -> str:
        return f'sql("{self.sql}")'

    def to_wire_format(self) -> dict:
        return {
            **super().to_wire_format(),
            "subType": "sqlText",
            "sql": self.sql,
        }

    @classmethod
    def from_wire_format(cls, wire: dict) -> "SqlTextColumnExpression":
        assert wire["subType"] == "sqlText"
        result = SqlTextColumnExpression(wire["sql"])
        result._from_wire_format_shared(wire)
        return result
