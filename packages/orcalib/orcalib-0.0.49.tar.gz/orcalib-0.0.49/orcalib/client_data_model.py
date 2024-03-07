from typing import Any, Optional, TypedDict, Union

import numpy as np
import pandas
from orca_common import ColumnName, Order, OrderByColumns, RowDict
from pydantic import BaseModel


class ApiFilter(BaseModel):
    """Client-side model of a filter that's used with calls to `select(...)`
    NOTE: It doesn't look like we're actually using filters on the client-side anywhere.
    """

    op: str
    args: list[Union[str, int, float, bool, "ApiFilter"]]


# Type alias for various types of row data that can be passed to the insert/update/upsert function.
RowData = RowDict | pandas.DataFrame | list[RowDict]
OrderByColumn = ColumnName | tuple[ColumnName, Order]


class SimpleTableQueryRequest(BaseModel):
    """Client-side model of the request to the `simple_table_query` endpoint.
    NOTE: This is currently a duplicate of the server's model, but we want them to
    remain separate for now, since the client's model may change in the future.
    """

    columns: Optional[list[str]] = None
    limit: Optional[int] = None
    filter: Optional[ApiFilter] = None
    order_by_columns: Optional[OrderByColumns] = None
    default_order: Order = Order.ASCENDING


class TableRowResponse(TypedDict):
    row_id: int
    column_values: dict[ColumnName, Any]


class TableSelectResponse(TypedDict):
    """Client-side model of the response from the `simple_table_query` endpoint."""

    status_code: int
    rows: list[TableRowResponse]


def decode_ndarray(obj):
    """Decode a JSON object that was encoded with `encode_ndarray`.
    TODO: This needs to be generalized to use the type handles to decode column types.
    """
    if "__ndarray__" in obj:
        return np.array(obj["__ndarray__"])
    return obj
