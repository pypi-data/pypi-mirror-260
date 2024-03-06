from typing import *
from abc import ABC

from ..utils.serializable import Serializable


class Source(ABC, Serializable):
    """
    Represents the underlying data table for a Model.
    Consumers should not interact with this class directly,
    instead modifying the table through methods on the model.

    When attaching a source, use `table` to reference a physical
    table inside the database, or `sql` to select from a SQL subquery.
    """

    def to_wire_format(self) -> dict:
        return {"type": "source", "subType": "<ABSTRACT_BASE>"}

    @classmethod
    def from_wire_format(cls, wire: dict) -> "Source":
        assert wire["type"] == "source"
        if wire["subType"] == "tableName":
            return TableNameSource.from_wire_format(wire)
        elif wire["subType"] == "sqlText":
            return SqlTextSource.from_wire_format(wire)
        elif wire["subType"] == "transform":
            from .source_transform import TransformedSource

            return TransformedSource.from_wire_format(wire)
        else:
            raise AssertionError("Unknown Source subType: " + wire["subType"])

    def _default_identifier(self) -> Optional[str]:
        return None


def table(sql: str) -> "TableNameSource":
    """
    Constructs a Source with the provided table as its contents.
    This name will be escaped according to the database dialect, and
    always be correctly scoped.
    """
    return TableNameSource(sql)


class TableNameSource(Source):
    def __init__(self, table_name: str) -> None:
        super().__init__()
        self.table_name = table_name

    def _default_identifier(self) -> Optional[str]:
        first_token = self.table_name.split(".")[0]
        if first_token.isidentifier():
            return first_token
        return None

    def __repr__(self) -> str:
        return f"`{self.table_name}`)"

    def to_wire_format(self) -> dict:
        return {
            **super().to_wire_format(),
            "subType": "tableName",
            "tableName": self.table_name,
        }

    @classmethod
    def from_wire_format(cls, wire: dict) -> "TableNameSource":
        assert wire["subType"] == "tableName"
        return TableNameSource(wire["tableName"])


class SqlTextSource(Source):
    def __init__(self, sql: str) -> None:
        super().__init__()
        self.sql = sql

    def _default_identifier(self) -> Optional[str]:
        # maybe inspect the SQL to look for a table name?
        return None

    def __repr__(self) -> str:
        return f'sql("{self.sql}")'

    def to_wire_format(self) -> dict:
        return {
            **super().to_wire_format(),
            "subType": "sqlText",
            "sql": self.sql,
        }

    @classmethod
    def from_wire_format(cls, wire: dict) -> "SqlTextSource":
        assert wire["subType"] == "sqlText"
        return SqlTextSource(wire["sql"])
