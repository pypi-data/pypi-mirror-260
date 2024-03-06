from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Literal, Union, overload

from ..hashboard_api.api import HashboardAPI

if TYPE_CHECKING:
    from ..model.model import Model  # avoid circular dep


@overload
def run(
    model: Model,
    format: Union[None, Literal["list"]] = None,
) -> List[Dict[str, Any]]:
    """
    Executes the model, returning the resultant rows
    as a list of Python values.
    """
    ...


@overload
def run(
    model: Model,
    format: Literal["sql"],
) -> str:
    """
    Generates the SQL query which would be issued to execute
    this model.
    """
    ...


def run(model: Model, format: Union[None, Literal["list"], Literal["sql"]] = None):
    """
    Executes the model, returning the resultant rows
    as a list of Python values.

    If `format='sql'` will instead return the SQL query
    that would be executed.
    """
    api = HashboardAPI()
    executor = {
        "list": "default",
        "sql": "sql",
    }.get(format) or "default"
    result = api.post(
        "db/v2/execute-model",
        {
            "model": model.to_wire_format(),
            "projectId": api.project_id,
            "executor": executor,
        },
    )
    return result
