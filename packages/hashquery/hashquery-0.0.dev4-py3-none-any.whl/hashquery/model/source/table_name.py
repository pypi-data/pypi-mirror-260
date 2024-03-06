from typing import *

from .source import Source


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

    __TYPE_KEY__ = "tableName"

    def to_wire_format(self) -> dict:
        return {
            **super().to_wire_format(),
            "tableName": self.table_name,
        }

    @classmethod
    def from_wire_format(cls, wire: dict) -> "TableNameSource":
        assert wire["subType"] == cls.__TYPE_KEY__
        return TableNameSource(wire["tableName"])
