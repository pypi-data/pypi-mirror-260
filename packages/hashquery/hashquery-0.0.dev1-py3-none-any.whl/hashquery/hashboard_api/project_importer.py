import builtins
from contextlib import contextmanager
from typing import Any, Callable, List, Optional, cast

from ..model.model import Model
from ..utils.resource import LinkedResource
from . import HashboardAPI


class ProjectImporter:
    """
    Utility for fetching resources from a Hashboard project.
    """

    # --- business logic to load and parse resources ---

    def __init__(self) -> None:
        self._cached_data_connections: Optional[List[LinkedResource]] = None
        self._cached_models: Optional[List[Any]] = None

    # -- models --

    def model_by_alias(self, alias: str) -> Optional[Model]:
        """
        Fetches a `Model` which has the provided alias, or `None` if no model
        has that alias.
        """
        models = self.all_models()
        for model in models:
            if model.linked_resource.alias == alias:
                return model
        return None

    def all_models(self) -> List[Model]:
        """
        Fetches all the models in the project.
        """
        if self._cached_models is not None:
            return self._cached_models

        api = HashboardAPI()
        wire_models = api.graphql(
            """
            query HashqueryModels($projectId: String!) {
                hashqueryModels(projectId: $projectId)
            }
            """,
            {"projectId": api.project_id},
        )["data"]["hashqueryModels"]
        self._cached_models = [Model.from_wire_format(wire) for wire in wire_models]
        return self._cached_models

    # -- data connections --

    def data_connection_by_alias(self, alias: str) -> Optional[LinkedResource]:
        """
        Fetches a connection reference which has the provided alias, or `None`
        if no connection has that alias.
        """
        conns = self.all_data_connections()
        for conn in conns:
            if conn.alias == alias:
                return conn
        return None

    def all_data_connections(self) -> List[LinkedResource]:
        """
        Fetches all the data connections in the project.
        """
        if self._cached_data_connections is not None:
            return self._cached_data_connections

        api = HashboardAPI()
        raw_data_connections = api.graphql(
            """
            query HashqueryDataConnections($projectId: String!) {
                dataConnections(projectId: $projectId) { id, name }
            }
            """,
            {"projectId": api.project_id},
        )["data"]["dataConnections"]
        self._cached_data_connections = [
            LinkedResource(
                id=wire["id"],
                # currently, DataConnections do not have aliases, so just use
                # the lowercased name and snake-spaced
                alias=cast(str, wire["name"]).replace(" ", "_").lower(),
            )
            for wire in raw_data_connections
        ]
        return self._cached_data_connections

    # --- import hook ---

    def _get_package_importers(self):
        # map of `subpackage name --> [item_getter, all_getter]`
        return {
            "connections": [
                self.data_connection_by_alias,
                self.all_data_connections,
            ],
            "models": [
                self.model_by_alias,
                self.all_models,
            ],
        }

    @classmethod
    @contextmanager
    def import_context(cls, root: str = "project"):
        importer = cls()
        base_import = builtins.__import__
        builtins.__import__ = importer._get_import_override(root, base_import)
        try:
            yield
        finally:
            builtins.__import__ = base_import

    def _get_import_override(self, root: str, base_import: Callable):
        package_importers_map = self._get_package_importers()

        def _custom_import(package: str, g=None, l=None, names=None, i=0):
            if package == root:
                raise ImportError(
                    f"Import against `{root}` must include a subpackage, such as `{root}.models`"
                )
            elif package.startswith(f"{root}."):
                package_parts = package.split(".")
                if not len(package_parts) == 2:
                    raise ImportError(
                        f"No such package {package}.\n"
                        + f"Did you mean `from {'.'.join(package_parts[:2])} import {package_parts[2]}`?"
                    )
                subpackage = package_parts[1]
                subpackage_getters = package_importers_map.get(subpackage)
                if not subpackage_getters:
                    raise ImportError(f"No such package {package}.\n")
                subpackage_get_one, subpackage_get_all = subpackage_getters
                get_alias = lambda item: (
                    item.alias if hasattr(item, "alias") else item.linked_resource.alias
                )
                if names:
                    return DictAsModule(
                        {
                            get_alias(item): item
                            for item in [
                                required_import(
                                    subpackage_get_one(name), name, subpackage
                                )
                                for name in names
                            ]
                        }
                    )
                else:
                    return DictAsModule(
                        {
                            subpackage: DictAsModule(
                                {get_alias(item): item for item in subpackage_get_all()}
                            )
                        }
                    )
            else:
                return base_import(package, g, l, names, i)

        return _custom_import


def required_import(value, requested_identifier, subpackage):
    if value is None:
        raise ImportError(f"`{requested_identifier}` not found in `{subpackage}`")
    return value


class DictAsModule:
    def __init__(self, dict_ref) -> None:
        self.__dict__ = dict_ref
        self.__module__ = "<hashboard_import>"
