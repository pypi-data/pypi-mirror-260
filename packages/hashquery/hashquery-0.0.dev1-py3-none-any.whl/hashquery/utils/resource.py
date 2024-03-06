from typing import *

from .serializable import Serializable


class LinkedResource(Serializable):
    """
    Represents a reference to an external resource.
    Consumer code will most commonly interact with this object to represent
    a data connection loaded with :py:func:`~hashquery.project_importer.ProjectImporter.data_connection_by_alias`
    """

    def __init__(self, id: str, alias: Optional[str] = None) -> None:
        self.id = id
        self.alias = alias

    def to_wire_format(self) -> dict:
        return {"id": self.id, "alias": self.alias}

    @classmethod
    def from_wire_format(cls, wire: dict):
        return LinkedResource(id=wire["id"], alias=wire.get("alias"))
