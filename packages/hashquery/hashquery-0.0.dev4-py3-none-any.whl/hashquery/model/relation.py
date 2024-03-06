from typing import *

from .column_expression import ColumnExpression
from ..utils.identifiable import Identifiable
from ..utils.serializable import Serializable


class ModelRelation(Serializable, Identifiable):
    def __init__(
        self,
        joined_model,
        join_condition: ColumnExpression,
        identifier: str,
        *,
        drop_unmatched: bool = False,
    ) -> None:
        from .model import Model  # circular reference

        self.joined_model: Model = joined_model
        self.join_condition = join_condition
        self.identifier = identifier
        self.drop_unmatched = drop_unmatched

    # proxy accessing nested properties
    def __getattr__(self, name: str) -> Any:
        # use standard lookup for these keys, else this could result
        # in an infinite loop (since this function references them)
        if name.startswith("__") or name in ["joined_model"]:
            raise AttributeError()

        attr = self.joined_model.attributes[name]
        return attr.disambiguated(self)

    # --- Serialization ---

    def to_wire_format(self) -> Dict:
        return {
            "type": "modelRelation",
            "identifier": self.identifier,
            "joinedModel": self.joined_model.to_wire_format(),
            "joinCondition": self.join_condition.to_wire_format(),
            "dropUnmatched": self.drop_unmatched,
        }

    @classmethod
    def from_wire_format(cls, wire: Dict) -> "ModelRelation":
        from .model import Model

        assert wire["type"] == "modelRelation"
        return ModelRelation(
            Model.from_wire_format(wire["joinedModel"]),
            ColumnExpression.from_wire_format(wire["joinCondition"]),
            identifier=wire["identifier"],
            drop_unmatched=wire.get("dropUnmatched"),
        )
