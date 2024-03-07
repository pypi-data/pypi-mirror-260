from __future__ import annotations
from typing import TYPE_CHECKING, Any, Dict, List, Literal, Union, overload
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Literal, Union, overload

from ..hashboard_api.api import HashboardAPI
from .run_results import RunResults
from ..hashboard_api.api import HashboardAPI

if TYPE_CHECKING:
    from ..model.model import Model  # avoid circular dep


def run(
    model: "Model",
    *,
    freshness: Optional[datetime] = None,
    print_warnings: bool = True,
    print_exec_stats: bool = False,
) -> RunResults:
    """
    Executes the model.
    This compiles and runs a query within the model's database, and returns
    an object which can be used to view result rows and query metadata.

    `freshness` can be used to control the minimum timestamp of any caches
    used during execution.
    """
    result_json = _post_run_endpoint(model, freshness=freshness)
    return RunResults(
        result_json,
        print_warnings=print_warnings,
        print_exec_stats=print_exec_stats,
    )


def compile_sql(
    model: "Model",
    *,
    freshness: Optional[datetime] = None,
    print_warnings: bool = True,
) -> str:
    """
    Compiles the SQL that would be run if you executed this Model with
    `run` and returns it as a string. Nothing will be sent to the database.

    This SQL query does not use parameterization, and so it may be prone to
    SQL injection if you were to execute it directly. If your intent is
    to execute the model, use the `run` API instead.

    `freshness` can be used to control the minimum timestamp of any caches
    used during compilation.
    """
    result_json = _post_run_endpoint(model, sql_only=True, freshness=freshness)
    return RunResults(
        result_json, print_warnings=print_warnings, print_exec_stats=False
    ).sql_query


def _post_run_endpoint(
    model: "Model",
    *,
    sql_only: bool = False,
    freshness: Optional[datetime] = None,
):
    api = HashboardAPI()
    return api.post(
        "db/v2/execute-model",
        {
            "model": model.to_wire_format(),
            "projectId": api.project_id,
            "options": {
                "sqlOnly": sql_only,
                "freshness": freshness.isoformat() if freshness else None,
            },
        },
    )
