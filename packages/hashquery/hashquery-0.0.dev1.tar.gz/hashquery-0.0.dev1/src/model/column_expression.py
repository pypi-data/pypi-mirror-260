from typing import *
from abc import ABC, abstractmethod

from ..utils.builder import builder_method
from ..utils.serializable import Serializable
from ..utils.identifiable import Identifiable
from ..utils.keypath import KeyPath, unwrap_keypath_to_name

if TYPE_CHECKING:
    from .relation import ModelRelation


class ColumnExpression(ABC, Identifiable, Serializable):
    def __init__(self) -> None:
        super().__init__()
        self._manually_set_identifier: Optional[str] = None

    # --- Identifier Management ---

    @abstractmethod
    def default_identifier(self) -> Optional[str]:
        ...

    @builder_method
    def named(self, name: Union[str, KeyPath]) -> "ColumnExpression":
        """
        Forms a copy of this column expression with a new name.
        The name of a column expression will be the identifier when attached
        to a Model with `with_attribute` or `with_measure`. When queried, this
        will be analogous to an `AS <name>` clause.
        """
        name = unwrap_keypath_to_name(name)
        self._manually_set_identifier = name

    @property
    def identifier(self) -> str:
        found_id = self._optional_identifier
        if not found_id:
            raise AssertionError(
                f"{self} has no identifier and a default cannot be determined. "
                + "Call `.named()` to provide an identifier for this expression."
            )
        return found_id

    @property
    def _optional_identifier(self) -> bool:
        return self._manually_set_identifier or self.default_identifier()

    # --- Scoping ---

    @abstractmethod
    @builder_method
    def disambiguated(
        self, namespace: Union["ModelRelation", str]
    ) -> "ColumnExpression":
        """
        Some column expressions require scoping to a namespace, to avoid
        conflicting names. For example, a `column("id")` expression refers to
        different values when qualified with one table `sales.id` vs. another
        `customers.id`, despite being otherwise the same definition.

        `.disambiguated` can be used to identify what namespace a given column
        expression needs to be qualified with.

        If a column expression has not had `disambiguated` applied, it may
        still appear fully qualified in the final query, typically scoped to
        the namespace of the model being invoked (ie. the contents of the
        `FROM` clause).
        """
        ...

    # --- Serialization ---

    def to_wire_format(self) -> Any:
        return {
            "type": "columnExpression",
            "subType": "<ABSTRACT_BASE>",
            "manuallySetIdentifier": self._manually_set_identifier,
            # `__denormalized` contains content that non-Python consumers may
            # need, but which a Py consumer should never read off, since this
            # data is derivable from the instance's methods. These values should
            # not be read inside of `from_wire_format`.
            "__denormalized": {"identifier": self._optional_identifier},
        }

    @classmethod
    def from_wire_format(cls, wire: dict):
        from .column_expression_func import ApplyFunctionColumnExpression
        from .column_expression_transform import TransformedColumnExpression
        from .column_expression_operators import BinaryOpColumnExpression
        from .column_expression_sql import (
            ColumnNameColumnExpression,
            SqlTextColumnExpression,
            PyValueColumnExpression,
        )

        assert wire["type"] == "columnExpression"
        if wire["subType"] == "columnName":
            return ColumnNameColumnExpression.from_wire_format(wire)
        elif wire["subType"] == "pyValue":
            return PyValueColumnExpression.from_wire_format(wire)
        elif wire["subType"] == "sqlText":
            return SqlTextColumnExpression.from_wire_format(wire)
        elif wire["subType"] == "transform":
            return TransformedColumnExpression.from_wire_format(wire)
        elif wire["subType"] == "binaryOp":
            return BinaryOpColumnExpression.from_wire_format(wire)
        elif wire["subType"] == "applyFunction":
            return ApplyFunctionColumnExpression.from_wire_format(wire)
        else:
            raise AssertionError("Unknown ColumnExpression subType: " + wire["subType"])

    def _from_wire_format_shared(self, wire: dict):
        self._manually_set_identifier = wire["manuallySetIdentifier"]

    # --- Chained Transforms ---

    # - Granularity -

    def by_granularity(self, granularity: str) -> "ColumnExpression":
        from .column_expression_transform import GranularityColumnExpression

        return GranularityColumnExpression(self, granularity)

    @property
    def by_second(self) -> "ColumnExpression":
        """
        Truncate the target time column to the containing second.
        """
        return self.by_granularity("second")

    @property
    def by_minute(self) -> "ColumnExpression":
        """
        Truncate the target time column to the containing minute.
        """
        return self.by_granularity("minute")

    @property
    def by_hour(self) -> "ColumnExpression":
        """
        Truncate the target time column to the containing hour.
        """
        return self.by_granularity("hour")

    @property
    def by_day(self) -> "ColumnExpression":
        """
        Truncate the target time column to the containing day.
        """
        return self.by_granularity("day")

    @property
    def by_week(self) -> "ColumnExpression":
        """
        Truncate the target time column to the containing week.
        Sunday is considered the start of the week by default, though this can
        be changed in the Hashboard project's settings.
        """
        return self.by_granularity("week")

    @property
    def by_quarter(self) -> "ColumnExpression":
        """
        Truncate the target time column to the containing quarter.
        """
        return self.by_granularity("quarter")

    @property
    def by_year(self) -> "ColumnExpression":
        """
        Truncate the target time column to the containing year.
        """
        return self.by_granularity("year")

    # - Operators -

    def _binary_op(self, other: object, op: str) -> "ColumnExpression":
        from .column_expression_operators import BinaryOpColumnExpression
        from .column_expression_sql import PyValueColumnExpression

        if not isinstance(other, ColumnExpression):
            other = PyValueColumnExpression(other)
        return BinaryOpColumnExpression(self, other, op)

    def __eq__(self, other: object):
        return self._binary_op(other, "=")

    def __ne__(self, other: object):
        return self._binary_op(other, "!=")

    def __lt__(self, other: object):
        return self._binary_op(other, "<")

    def __le__(self, other: object):
        return self._binary_op(other, "<=")

    def __gt__(self, other: object):
        return self._binary_op(other, ">")

    def __ge__(self, other: object):
        return self._binary_op(other, ">=")

    def __add__(self, other: object):
        return self._binary_op(other, "+")

    def __sub__(self, other: object):
        return self._binary_op(other, "-")

    def __mul__(self, other: object):
        return self._binary_op(other, "*")

    def __truediv__(self, other: object):
        return self._binary_op(other, "/")

    def __and__(self, other: object):
        return self._binary_op(other, "AND")

    def __or__(self, other: object):
        return self._binary_op(other, "OR")
