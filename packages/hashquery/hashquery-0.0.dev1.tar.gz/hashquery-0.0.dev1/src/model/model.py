from typing import *

from ..utils.access_proxy import AccessProxy
from ..utils.iterator import iterate_deep_source_traversal
from ..utils.builder import builder_method
from ..utils.serializable import Serializable
from ..utils.keypath import (
    _,
    resolve_keypath_args_from,
    resolve_keypath,
    unwrap_keypath_to_name,
    KeyPath,
)
from ..utils.identifiable import (
    Identifiable,
    IdentifiableMap,
)
from ..utils.resource import LinkedResource
from .column_expression import ColumnExpression
from .column_expression_sql import (
    SqlTextColumnExpression,
    ColumnNameColumnExpression,
    column,
)
from .source import Source, SqlTextSource
from .relation import ModelRelation
from .source_transform import (
    AggregateSource,
    FilterSource,
    SelectSource,
    SortSource,
    LimitSource,
    JoinOneSource,
)


class Model(Serializable, Identifiable):
    def __init__(self) -> None:
        self.connection: LinkedResource = None
        self.source: Source = None
        self.attributes = IdentifiableMap[ColumnExpression]()
        self.measures = IdentifiableMap[ColumnExpression]()
        self.relations = IdentifiableMap[ModelRelation]()
        self.primary_key: ColumnExpression = column("id")
        self.custom_meta = {}
        # internally used to understand the origin of a model
        # and its relation to an original Hashboard resource
        self.linked_resource: Optional[LinkedResource] = None

    # allow accessing nested properties via direct `.` access
    # instead of always going through `model.attributes.` or similar
    def __getattr__(self, name: str) -> Any:
        # use standard lookup for these keys, else this could result
        # in an infinite loop (since this function references them)
        if name.startswith("__") or name in ["attributes", "measures", "relations"]:
            raise AttributeError()

        maps: List[IdentifiableMap] = [self.attributes, self.measures, self.relations]
        matches = [i for i in [map.get(name) for map in maps] if i is not None]
        # TODO: if we don't find anything here, and our source is a SQL thing,
        # we should just assume there's an attribute with that name, and
        # optimistically return a ColumnExpression with `column(name)`.
        # That way you don't need to define all the physical columns of your
        # model in order to reference them.
        matched_count = len(matches)
        if matched_count == 1:
            return matches[0]
        if matched_count == 0:
            raise AttributeError(
                f"Model has no attribute, measure, or relation with name '{name}'"
            )
        else:
            raise AttributeError(
                f"'{name}' is ambiguous on model. "
                + f"{matched_count} attributes, measures, or relations share that name. "
                + "Rename one of the properties with `named`."
            )

    # --- Adding Properties ---

    @builder_method
    def with_data_source(
        self,
        connection: LinkedResource,
        source: Union[Source, SqlTextColumnExpression],
    ) -> "Model":
        """
        Forms a new Model with the provided data source as the underlying table.
        If the receiver already had a source attached, this overwrites that
        reference, including any transformations to that source.

        If you want to join or union multiple datasets, use
        `Model.with_join_one` or `Model.union`.
        """
        self.connection = connection
        if type(source) is SqlTextColumnExpression:
            # We accept `SqlTextColumnExpression` here and convert it to a
            # `SqlTextSource`. This is because the free function
            # `sql("...")` would be a reasonable thing to pass into
            # this, and that returns a `ColumnExpression`.
            # If only we had contextual typing! I miss Swift...      :'(
            source = SqlTextSource(source.sql)
        self.source = source

    @builder_method
    @resolve_keypath_args_from(_.self)
    def with_attribute(self, expression: Union[ColumnExpression, str]) -> "Model":
        """
        Forms a new Model with the provided column expression included as an
        attribute. If a string is passed, this will interpret it as a column
        name if it is a valid identifier, else as literal SQL.
        """
        if type(expression) == str:
            expression = (
                ColumnNameColumnExpression(expression)
                if expression.isidentifier()
                else SqlTextColumnExpression(expression)
            )
        self.attributes.add(expression)

    @builder_method
    @resolve_keypath_args_from(_.self)
    def with_primary_key(self, expression: Union[ColumnExpression, str]) -> "Model":
        """
        Forms a new model with the provided column expression configured as the
        primary key. This should be a unique value across all records in the
        source. By default, this is `column("id")`.
        """
        if type(expression) == str:
            expression = (
                ColumnNameColumnExpression(expression)
                if expression.isidentifier()
                else SqlTextColumnExpression(expression)
            )
        self.primary_key = expression

    @builder_method
    @resolve_keypath_args_from(_.self)
    def with_measure(self, expression: ColumnExpression) -> "Model":
        """
        Forms a new Model with the provided column expression included as a
        measure definition. This does not perform any aggregation on its own,
        this just attaches a definition for later use.
        """
        self.measures.add(expression)

    @builder_method
    def with_join_one(
        self,
        joined: "Model",
        *,
        on: Optional[Union[ColumnExpression, KeyPath]] = None,
        condition: Callable[
            ["ModelAttributes", "ModelAttributes"],
            ColumnExpression,
        ] = None,
        named: Optional[Union[str, KeyPath]] = None,
        drop_unmatched: bool = False,
    ) -> "Model":
        """
        Forms a new Model with a new property which can be used to reference
        the properties of the `joined` Model. Records are aligned using `condition`.

        Similar to `with_measure` and `with_attribute`, `with_join_one` has no
        performance cost on its own. No JOIN statement is added to queries
        unless the relation is actually referenced.

        This never changes the record count of the data by exploding rows.
        If multiple records match, only the first matching record is joined.
        If you want to explode records, use `Model.cross_join` instead.

        If no records match, `NULL` values are filled in for the missing columns,
        unless `drop_unmatched=True` is passed.
        """
        # -- gather all the parameters up, resolve and validate --
        if on is None and condition is None:
            raise ValueError(
                "`.with_join_one` must specify a join condition using "
                + "`on=<foreign_key>` and/or `condition=<column_expression>`"
            )
        if type(joined) == KeyPath:
            joined = resolve_keypath(self, joined)
        relation_name = unwrap_keypath_to_name(named)
        if not relation_name:
            for source in iterate_deep_source_traversal(joined.source):
                if default_identifier := source._default_identifier():
                    relation_name = default_identifier
        if not relation_name:
            raise ValueError(
                "Join was not provided an identifier and a default could not be inferred. "
                + "Provide an explicit name for this relation using `named=`"
            )

        # -- determine the column expression to join with --
        join_predicate = None
        if on is not None:
            on: ColumnExpression = (
                resolve_keypath(self, on) if (type(on) == KeyPath) else on
            )
            join_predicate = on == joined.primary_key.disambiguated(relation_name)
        if condition is not None:
            condition_predicate = condition(
                # within the condition expression, only attributes can be
                # accessed, and disambiguate the right-side
                AccessProxy(self.attributes),
                AccessProxy(
                    joined.attributes,
                    lambda c: c.disambiguated(relation_name),
                ),
            )
            join_predicate = (
                condition_predicate
                if not join_predicate
                else join_predicate & condition_predicate
            )

        # -- attach the final relation --
        relation = ModelRelation(
            joined,
            join_predicate,
            identifier=relation_name,
            drop_unmatched=drop_unmatched,
        )
        self.source = JoinOneSource(base=self.source, relation=relation)
        self.relations.add(relation)

    @builder_method
    @resolve_keypath_args_from(_.self)
    def with_custom_meta(self, name: str, value: Any) -> "Model":
        """
        Forms a new Model with the custom metadata attached on `.custom_meta[name]`.
        Hashboard will never read or write to the `custom_meta` dictionary, making
        it a good spot to put any custom configuration or encode semantic information
        about the Model you can use later.
        """
        self.custom_meta[name] = value

    # --- Analysis ---

    @builder_method
    @resolve_keypath_args_from(_.self)
    def aggregate(
        self,
        *,
        groups: List[ColumnExpression] = None,
        measures: List[ColumnExpression] = None,
    ) -> "Model":
        self.source = AggregateSource(self.source, groups=groups, measures=measures)
        self.attributes = IdentifiableMap(
            column(c.identifier) for c in groups + measures
        )
        self.measures = IdentifiableMap()
        self.relations = IdentifiableMap()

    # --- Record Management ---

    @builder_method
    @resolve_keypath_args_from(_.self)
    def select(self, attributes: List[ColumnExpression]) -> "Model":
        """
        Forms a new Model with only the included attributes included.
        Measures are unaffected.
        """
        self.source = SelectSource(self.source, attributes)
        self.attributes = IdentifiableMap(attributes)
        # TODO: if a relation is referenced here, we should maintain it,
        # but otherwise drop it (or just inline only the referenced fields?)
        self.relations = IdentifiableMap()

    @builder_method
    @resolve_keypath_args_from(_.self)
    def filter(self, condition: ColumnExpression) -> "Model":
        """
        Forms a new Model with records filtered to only those which
        match the given condition.
        """
        self.source = FilterSource(self.source, condition)

    @builder_method
    @resolve_keypath_args_from(_.self)
    def sort(self, sort: ColumnExpression) -> "Model":
        """
        Forms a new Model with records ordered by the provided column.
        """
        self.source = SortSource(self.source, sort)

    @builder_method
    @resolve_keypath_args_from(_.self)
    def take(self, count: int) -> "Model":
        """
        Forms a new Model with only the first N records.
        """
        self.source = LimitSource(self.source, count)

    # --- Serialization ---

    def to_wire_format(self) -> dict:
        return {
            "type": "model",
            "connection": self.connection.to_wire_format(),
            "source": self.source.to_wire_format(),
            "attributes": [a.to_wire_format() for a in self.attributes],
            "measures": [m.to_wire_format() for m in self.measures],
            "relations": [r.to_wire_format() for r in self.relations],
            "primaryKey": self.primary_key.to_wire_format(),
            "customMeta": self.custom_meta,
            "linkedResource": (
                self.linked_resource.to_wire_format() if self.linked_resource else None
            ),
        }

    @classmethod
    def from_wire_format(cls, wire: dict):
        assert wire["type"] == "model"
        result = Model()
        result.connection = LinkedResource.from_wire_format(wire["connection"])
        result.source = Source.from_wire_format(wire["source"])
        result.attributes = IdentifiableMap(
            ColumnExpression.from_wire_format(a) for a in wire.get("attributes", [])
        )
        result.measures = IdentifiableMap(
            ColumnExpression.from_wire_format(m) for m in wire.get("measures", [])
        )
        result.relations = IdentifiableMap(
            ModelRelation.from_wire_format(r) for r in wire.get("relations", [])
        )
        result.primary_key = ColumnExpression.from_wire_format(wire["primaryKey"])
        result.custom_meta = wire.get("customMeta", {})
        result.linked_resource = (
            LinkedResource.from_wire_format(wire["linkedResource"])
            if wire["linkedResource"]
            else None
        )
        return result


ModelAttributes = AccessProxy["Model", ColumnExpression]
