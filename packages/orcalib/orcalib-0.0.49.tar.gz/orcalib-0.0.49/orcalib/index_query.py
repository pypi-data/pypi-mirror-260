from typing import Any, Iterator, Optional

import numpy as np
import pandas
import torch
from orca_common import ColumnName
from orcalib.client import OrcaClient, default_api_version_key
from orcalib.client_data_model import RowDict
from orcalib.data_classes import VectorScanResult
from orcalib.index_handle import IndexHandle
from orcalib.orca_expr import OrcaExpr
from orcalib.orca_types import NumericTypeHandle
from orcalib.table import TableHandle
from orcalib.table_query import TableQuery

IndexName = str


class BatchedVectorScanResult:
    """A batched vector scan result, containing batches of memory results. Each
    memory result contains its embedding vector and any additional columns that
    were requested in the query.

    This class acts as a view on the underlying data, allowing you to slice it
    by batch, memory, and column. The slicing is lazy, so it doesn't copy any
    of the underlying data.
    """

    # The name of the special column that contains the embedding vector
    VECTOR_KEY = "__vector__"
    _special_key_count = 1
    # TODO: Add additional special columns, e.g., "distance from query vector"

    # A slice into a column. Can be a single column name, a list of column names
    # or indices, or a slice of column indices.
    ColumnSlice = slice | int | list[int] | ColumnName | list[ColumnName]

    def __init__(
        self,
        extra_col_names: list[ColumnName],
        data: list[list[tuple[Any, ...]]],
        batch_slice: slice | int | None = None,
        memory_slice: slice | int | None = None,
        column_slice: Optional[ColumnSlice] = None,
    ):
        """
        :param extra_col_names: The names of the extra columns that were requested in the query.
        :param data: The underlying data. This is a list of batches, where each batch is a list of memories,
        where each memory is a tuple of values.
        :param batch_slice: Used internally to maintain a "view" of the data based on a subset of the batches. You shouldn't need to set this manually.
        :param memory_slice: Used internally to maintain a "view" of the data based on a subset of the memories. You shouldn't need to set this manually.
        :param column_slice: Used internally to maintain a "view" of the data based on a subset of the columns. You shouldn't need to set this manually.
        """
        self.data = data

        self.batch_size = len(data)
        self.memories_per_batch = len(data[0]) if self.batch_size > 0 else 0

        if batch_slice is not None:
            assert isinstance(
                batch_slice, (slice, int)
            ), f"batch_slice must be a slice or int. You passed: {batch_slice}"
        if memory_slice is not None:
            assert isinstance(
                memory_slice, (slice, int)
            ), f"memory_slice must be a slice or int. You passed: {memory_slice}"
        if column_slice is not None:
            assert isinstance(
                column_slice, (slice, int, list, ColumnName)
            ), f"column_slice must be a slice, int, list, or ColumnName. You passed: {column_slice}"

        self.batch_slice = batch_slice
        self.memory_slice = memory_slice
        self.column_slice = column_slice

        self.extra_col_names = extra_col_names
        self.column_names = [self.VECTOR_KEY, *extra_col_names]
        self.column_to_index = {name: i for i, name in enumerate(self.column_names)}

    def _clone(self, **overrides) -> "BatchedVectorScanResult":
        """Clone this BatchedVectorScanResult, optionally overriding some parameters"""

        overrides["extra_col_names"] = overrides.get("extra_col_names", self.extra_col_names)
        overrides["data"] = overrides.get("data", self.data)
        overrides["batch_slice"] = overrides.get("batch_slice", self.batch_slice)
        overrides["memory_slice"] = overrides.get("memory_slice", self.memory_slice)
        overrides["column_slice"] = overrides.get("column_slice", self.column_slice)

        return BatchedVectorScanResult(**overrides)

    def _get_column_slice(self, batch_slice, memory_slice, column_slice) -> "BatchedVectorScanResult":
        """Helper function that slices the data based on the given batch, memory, and column slices.
        NOTE: When batch_slice and memory_slice are ints, this function doesn't return a BatchedVectorScanResult.
        Instead, if one column is selected, it returns a single value. If multiple columns are selected, it returns
        a list of values.
        """
        assert self.column_slice is None, f"BatchedVectorScanResult already fully sliced: {repr(self)}"

        if (
            isinstance(batch_slice, int)
            and isinstance(memory_slice, int)
            and isinstance(column_slice, (int, ColumnName))
        ):
            return self._extract_memory_values(self.data[batch_slice][memory_slice], column_slice)
        else:
            return self._clone(batch_slice=batch_slice, memory_slice=memory_slice, column_slice=column_slice)

    def _get_memory_slice(self, batch_slice, key: tuple | int) -> "BatchedVectorScanResult":
        """Helper function that slices the data based on the given batch and memory slices."""
        if self.memory_slice is not None:
            return self._get_column_slice(self.batch_slice, self.memory_slice, key)

        assert isinstance(key, (int, slice, tuple)), f"key must be an int, slice, or tuple. You passed: {key}"

        if isinstance(key, (int, slice)):
            return self._clone(batch_slice=batch_slice, memory_slice=key)

        key_length = len(key)
        if key_length == 1:
            return self._clone(batch_slice=batch_slice, memory_slice=key[0])
        elif key_length == 2:
            return self._get_column_slice(batch_slice, *key)
        else:
            raise ValueError(
                f"key must be a tuple with (memory_slice) or (memory_slice, column_slice). You passed: {key}"
            )

    def __getitem__(self, key) -> "BatchedVectorScanResult":
        """Slice the data based on the given batch, memory, and column slices.
        :param key: Key for indexing into the current BatchedVectorScanResult.
            - If we haven't sliced the data at all, then the key must be one of batch_slice,
              (batch_slice), (batch_slice, memory_slice), or (batch_slice, memory_slice, column_slice)
            - If batch_slice is already set, then the key must be one of memory_slice,
              (memory_slice), or (memory_slice, column_slice)
            - If batch_slice and memory_slice are already set, then the key must be a column_slice.
        A batch_slice can be a single batch index or a slice of batch indices.
        A memory_slice can be a single memory index or a slice of memory indices.
        A column_slice can be a single column name, a list of column names or indices, or a slice of column indices.
        :returns: A new BatchedVectorScanResult that is a view on the underlying data.
        NOTE: When batch_slice and memory_slice are ints, this function doesn't return a BatchedVectorScanResult.
        Instead, if one column is selected, it returns a single value. If multiple columns are selected,
        it returns a list of values.

        Examples:
        >>> # Slice the data by batch, memory, and column
        >>> first_batch = result[0] # Get the first batch
        >>> first_batch_last_memory = first_batch[-1:] # Get the last memory of the first batch
        >>> first_batch_last_memory_vector = first_batch_last_memory["__vector__"] # Get the vector of the last memory of the first batch
        >>> first_batch[-1:, "__vector__"] # Equivalent to the above
        >>> result[0, -1:, "__vector__"] # Equivalent to the above

        >>> result[0, -1:, ["__vector__", "col1"]] # Get the vector and col1 of the last memory of the first batch
        """
        if self.batch_slice is not None:
            return self._get_memory_slice(self.batch_slice, key)

        assert (
            self.memory_slice is None
        ), "Cannot slice a BatchedVectorScanResult with a memory_slice unless batch_slice is slready specified"
        assert (
            self.column_slice is None
        ), "Cannot slice a BatchedVectorScanResult with a column_slice unless batch_slice, memory_slice are already specified"

        assert isinstance(key, (int, slice, tuple)), f"key must be an int, slice, or tuple. You passed: {key}"
        if isinstance(key, (int, slice)):
            return self._clone(batch_slice=key)

        key_length = len(key)
        if key_length == 1:
            return self._clone(batch_slice=key[0])
        elif key_length == 2:
            return self._get_memory_slice(*key)
        elif key_length == 3:
            return self._get_column_slice(*key)
        else:
            raise ValueError(
                f"key must be a tuple with (batch_slice) or (batch_slice, memory_slice) or (batch_slice, memory_slice, column_slice). You passed: {key}"
            )

    def __repr__(self) -> str:
        """Return a string representation of this BatchedVectorScanResult"""
        if self.column_slice is not None:
            return f"BatchedVectorScanResult[{self.batch_slice},{self.memory_slice},{self.column_slice}]"
        elif self.memory_slice is not None:
            return f"BatchedVectorScanResult[{self.batch_slice},{self.memory_slice}]"
        elif self.batch_slice is not None:
            return f"BatchedVectorScanResult[{self.batch_slice}]"

        return f"BatchedVectorScanResult(batch_size={self.batch_size}, mem_count={self.memories_per_batch}, extra_col_names={self.extra_col_names})"

    # Need a function to convert the values of a vector column to a tensor with shape (batch_size, mem_count, vector_len)
    def to_tensor(
        self,
    ) -> torch.Tensor:
        """Convert the values of a vector column to a tensor with shape (batch_size, mem_count, vector_len)

        NOTE: This function only works when all of the following are true:
         -- The batch slice is a slice or None (i.e., not an int)
         -- The memory slice is a slice or None (i.e., not an int)
         -- The column_slice is None or a single column name or integer.
        NOTE: When column_slice is None, the tensor is built from the embedding vectors (i.e., the __vector__ column)
        """
        batch_slice, memory_slice, column = self._get_slices()

        # NOTE: We don't check for "None" here because None was converted to slice(None) in _get_slices()
        assert isinstance(batch_slice, slice), f"batch_slice must be a slice. You passed: {self.batch_slice}"
        assert isinstance(memory_slice, slice), f"memory_slice must be a slice. You passed: {self.memory_slice}"

        # The default column is the embedding vector
        if self.column_slice is None:
            column = self.VECTOR_KEY

        if isinstance(column, int):
            col_index = column
            assert col_index < len(self.column_names)
        elif isinstance(column, ColumnName):
            col_index = self.column_to_index.get(column, None)
            assert col_index is not None, f"column {column} not found in extra columns: {self.extra_col_names}"
        else:
            raise ValueError(f"column must be a single column name or integer. You passed: {column}")
        return torch.tensor(
            np.array([[row[col_index] for row in memories[memory_slice]] for memories in self.data[batch_slice]])
        )

    def _extract_memory_values(self, memory, column_slice: Optional[ColumnSlice]):
        """Helper function that extracts the values of the given column slice from the given memory
        NOTE: When column_slice is a single column, this function doesn't return a list. Instead, it returns
        a single value - might happen to be a list (e.g., if the column was a vector column)."""
        if column_slice is None:
            return memory[:]
        elif isinstance(column_slice, (int, slice)):
            return memory[column_slice]
        elif isinstance(column_slice, ColumnName):
            return memory[self.column_to_index[column_slice]]
        elif isinstance(column_slice, list):
            if all(isinstance(col, int) for col in column_slice):
                return [memory[col] for col in column_slice]
            elif all(isinstance(col, ColumnName) for col in column_slice):
                return [memory[self.column_to_index[col]] for col in column_slice]
            else:
                raise ValueError(
                    f"If column_slice is a list, all elements must be either ints or strings (but not a mix). You passed: {column_slice}"
                )
        else:
            raise ValueError(
                f"column_slice must be a slice, int, or list of ints or column names. You passed: {column_slice}"
            )

    def _get_slices(self) -> tuple[Any, Any, Any]:
        """Helper function that returns the effective batch, memory, and column slices"""
        batch_slice = self.batch_slice if self.batch_slice is not None else slice(None)
        memory_slice = self.memory_slice if self.memory_slice is not None else slice(None)
        column_slice = self.column_slice if self.column_slice is not None else slice(None)

        return batch_slice, memory_slice, column_slice

    def __len__(self) -> int:
        """Based on the current slices, return the number of batches, memories, or values in a vector column."""
        batch_slice, memory_slice, column_slice = self._get_slices()

        if isinstance(self.batch_slice, int):
            if self.memory_slice is int:
                return len(self._extract_memory_values(self.data[self.batch_slice][memory_slice], column_slice))
            else:
                return len(self.data[batch_slice][memory_slice])
        else:
            return len(self.data[batch_slice])

    def __iter__(self) -> Iterator:
        """Iterate over the batches of memories
        :returns: The return type depends on the current slices:
        - When batch_slice is an int (but memory_slice and column_slice are None), this yields each memory from that batch.
        - When batch_slice and memory_slice are both ints (but column_slice is None), this yields each value from that memory.
        - Otherwise, this yields each batch with the specified subset of selected memories/columns
        """
        batch_slice, memory_slice, column_slice = self._get_slices()

        if isinstance(batch_slice, int):
            if isinstance(memory_slice, int):
                yield from self._extract_memory_values(self.data[batch_slice][memory_slice], column_slice)
            else:
                yield from (
                    self._extract_memory_values(memory, column_slice) for memory in self.data[batch_slice][memory_slice]
                )
        else:
            yield from (
                [self._extract_memory_values(memory, column_slice) for memory in batch[memory_slice]]
                for batch in self.data[batch_slice]
            )

    def to_list(
        self,
    ) -> list[list[list[Any] | Any]]:
        """Convert the values of a vector column to a list of lists

        Example:
        >>> bsr[0].to_list() # returns the list of memories in the first batch
        >>> bsr[0, 0].to_list() # returns the list of "extra" column values in the first memory of the first batch.
        NOTE:The "special" keys like __vector__ are not included unless they're specifically requested.
        >>> bsr[0, 0, "col1"].to_list() # returns [value of col1] for the first memory of the first batch
        >>> bsr[0, 0, ["col1", "col2"]].to_list() # returns [value of col1, value of col2] for the first memory of the first batch
        >>> bsr[1:3, -2:, ["col1", "col2"]].to_list() # returns a list of lists of [value of col1, value of col2] for
        the last two memories of the second and third batches
        """
        batch_slice, memory_slice, column_slice = self._get_slices()

        if isinstance(batch_slice, int):
            if isinstance(memory_slice, int):
                value = self._extract_memory_values(self.data[batch_slice][memory_slice], column_slice)
                return value if isinstance(value, list) else [value]
            else:
                return [
                    self._extract_memory_values(memory, column_slice) for memory in self.data[batch_slice][memory_slice]
                ]
        else:
            return [
                [self._extract_memory_values(row, column_slice) for row in memories[memory_slice]]
                for memories in self.data[batch_slice]
            ]


class DefaultIndexQuery(TableQuery["DefaultIndexQuery"]):
    """A query on a (for now) single table. This is used to build up a query and then execute it with .fetch()"""

    def __init__(
        self,
        db_name: str,
        primary_table: TableHandle,
        # The name of the index to query
        # NOTE: Must be an index on primary_table
        index: IndexName,
        # The value to query the index for
        index_query: Any,
        index_value: Optional[ColumnName] = None,
        **kwargs,
    ):
        """
        Initialize a new index-based query on the given table.

        Args:
            db_name (str): The name of the database to query.
            primary_table (str): The primary table to query.
            columns (dict): The columns to select from each table.
            filter (str): The filter to apply to the query.
            order_by_columns (list of str): The columns to order by.
            limit (int): The maximum number of rows to return.
            default_order (str): The default order to use with "order_by" if no order is specified.
            index (IndexName): The name of the index to query.
            index_query (str): The value to query the index for.
            index_value (Optional[ColumnName]): The name of the column to store the index value in.
        """
        super().__init__(db_name, primary_table, **kwargs)
        self.index = index
        self.index_query = index_query
        self.index_value = index_value

    def _clone(self, **kwargs) -> "DefaultIndexQuery":
        """Clone this query, optionally overriding some parameters"""
        kwargs["index"] = kwargs.get("index", self.index)
        kwargs["index_query"] = kwargs.get("index_query", self.index_query)
        kwargs["index_value"] = kwargs.get("index_value", self.index_value)
        return super()._clone(**kwargs)

    @default_api_version_key("index.scan")
    def fetch(self, limit: int, api_version: Optional[str]) -> list[RowDict]:
        from orcalib.database import OrcaDatabase

        data = OrcaClient.scan_index(
            OrcaDatabase(self.db_name),
            self.index,
            self.index_query,
            limit=limit,
            columns=self.columns,
            api_version=api_version,
        )

        if self.index_value is not None:
            for row in data:
                row[self.index_value] = row["__index_value"]
                del row["__index_value"]
        return data

    def df(self, limit: Optional[int], explode: bool = False) -> pandas.DataFrame:
        """Fetch the results of this query as a pandas DataFrame"""
        ret = super().df(limit=limit)
        if explode and self.index_value is not None:
            ret = ret.explode(self.index_value, ignore_index=True)
        return ret


class VectorIndexQuery(TableQuery["VectorIndexQuery"]):
    def __init__(
        self,
        db_name: str,
        primary_table: TableHandle,
        index: IndexName,
        index_query: OrcaExpr,
        curate_run_ids: Optional[list[int]] = None,
        curate_layer_name: Optional[str] = None,
        **kwargs,
    ):
        """A query on a (for now) single table. This is used to build up a query and then execute it with .fetch()
        Args:
            db_name (str): The name of the database to query.
            primary_table (str): The primary table to query.
            columns (list[ColumnName]): The columns to select
            filter (str): The filter to apply to the query.
            order_by_columns (list of str): The columns to order by.
            limit (int): The maximum number of rows to return.
            default_order (str): The default order to use with "order_by" if no order is specified.
            index (IndexName): The name of the index to query.
            index_query (str): The value to query the index for.
            curate_run_ids (Optional[list[int]]): The run ids to use for curate.
            curate_layer_name (Optional[str]): The layer name to use for curate.
        """

        super().__init__(db_name, primary_table, **kwargs)
        self.index = index
        self.index_query = index_query
        self.curate_run_ids = curate_run_ids
        self.curate_layer_name = curate_layer_name

    def _clone(self, **kwargs) -> "VectorIndexQuery":
        """Clone this query, optionally overriding some parameters"""
        kwargs["index"] = kwargs.get("index", self.index)
        kwargs["index_query"] = kwargs.get("index_query", self.index_query)
        kwargs["curate_run_ids"] = kwargs.get("curate_run_ids", self.curate_run_ids)
        kwargs["curate_layer_name"] = kwargs.get("curate_layer_name", self.curate_layer_name)
        return super()._clone(**kwargs)

    @default_api_version_key("index.vector_scan")
    def fetch(self, limit: int, api_version: Optional[str]) -> BatchedVectorScanResult:
        data = OrcaClient.vector_scan_index(
            self.primary_table,
            self.index,
            self.index_query,
            limit=limit,
            columns=self.columns,
            curate_run_ids=self.curate_run_ids,
            curate_layer_name=self.curate_layer_name,
            api_version=api_version,
        )
        return data

    def track_with_curate(self, run_ids: list[int], layer_name: str):
        return self._clone(curate_run_ids=run_ids, curate_layer_name=layer_name)
