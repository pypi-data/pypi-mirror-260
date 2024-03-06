from typing import *


from .column_expression import ColumnExpression
from .py_value import PyValueColumnExpression
from ...utils.keypath import KeyPath, BoundKeyPath
from ...utils.keypath.keypath import KeyPath, BoundKeyPath, KeyPathComponentCall
from ...utils.builder import builder_method


# --- Public Exports


def count(target: Optional[Union[ColumnExpression, KeyPath, Any]] = None):
    """
    an aggregating `COUNT` expression over the provided column or value.
    You can omit a value to form `COUNT(*)`.
    """
    return _build_apply_function_expression("count", [target])


def distinct(target: Union[ColumnExpression, KeyPath]):
    """
    an aggregating `DISTINCT` expression over the provided column.
    """
    return _build_apply_function_expression("distinct", [target])


def max(target: Union[ColumnExpression, KeyPath]):
    """
    an aggregating `MAX` expression over the provided column.
    """
    return _build_apply_function_expression("max", [target])


def min(target: Union[ColumnExpression, KeyPath]):
    """
    an aggregating `MIN` expression over the provided column.
    """
    return _build_apply_function_expression("min", [target])


def sum(target: Union[ColumnExpression, KeyPath]):
    """
    an aggregating `AVG` expression over the provided column.
    """
    return _build_apply_function_expression("sum", [target])


def avg(target: Union[ColumnExpression, KeyPath]):
    """
    an aggregating `AVG` expression over the provided column.
    """
    return _build_apply_function_expression("avg", [target])


def _build_apply_function_expression(
    function_name: str, args: List[Any] = None, *, inherit_identifier=False
) -> "SqlFunctionColumnExpression":
    constructor = SqlFunctionColumnExpression
    if any(isinstance(arg, KeyPath) for arg in args):
        constructor = lambda *args, **kwargs: BoundKeyPath(
            SqlFunctionColumnExpression, [KeyPathComponentCall(args, kwargs)]
        )
    return constructor(function_name, args, inherit_identifier=inherit_identifier)


# --- Implementations ---


class SqlFunctionColumnExpression(ColumnExpression):
    def __init__(
        self,
        function_name: str,
        args: List[Any] = None,
        *,
        inherit_identifier=False,
    ) -> None:
        super().__init__()
        self.function_name = function_name
        self.args = args if args else []
        self.inherit_identifier = inherit_identifier
        if self.inherit_identifier:
            self._manually_set_identifier = (
                self._base_column_expression()._manually_set_identifier
            )

    def _base_column_expression(self) -> Optional[ColumnExpression]:
        for arg in self.args:
            if isinstance(arg, ColumnExpression):
                return arg
        return None

    def default_identifier(self) -> Optional[str]:
        base = self._base_column_expression()
        if self.inherit_identifier and base:
            return base.default_identifier()

        if base and type(base) != PyValueColumnExpression:
            base_default = base.default_identifier()
            if base_default:
                return f"{self.function_name}_{base_default}"

        return self.function_name

    @builder_method
    def disambiguated(self, namespace) -> "SqlFunctionColumnExpression":
        self.args = [
            arg.disambiguated(namespace) if isinstance(arg, ColumnExpression) else arg
            for arg in self.args
        ]

    def __repr__(self) -> str:
        return f"{self.function_name}({', '.join(str(arg) for arg in self.args)})"

    __TYPE_KEY__ = "sqlFunction"

    def to_wire_format(self) -> Any:
        return {
            **super().to_wire_format(),
            "functionName": self.function_name,
            "args": [
                arg.to_wire_format() if hasattr(arg, "to_wire_format") else arg
                for arg in self.args
            ],
            "inheritIdentifier": self.inherit_identifier,
        }

    @classmethod
    def from_wire_format(cls, wire: dict) -> "SqlFunctionColumnExpression":
        assert wire["subType"] == cls.__TYPE_KEY__

        function_name = wire["functionName"]
        args = [
            (
                ColumnExpression.from_wire_format(arg)
                if (type(arg) == dict and arg.get("type") == "columnExpression")
                else arg
            )
            for arg in wire["args"]
        ]
        return SqlFunctionColumnExpression(
            function_name,
            args,
            inherit_identifier=False,
        )._from_wire_format_shared(wire)
