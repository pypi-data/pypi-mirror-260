from typing import Any, Optional

from orca_common import TableCreateMode

from orcalib.database import with_default_database_method

from .client import OrcaClient
from .data_classes import VectorScanResult
from .database import OrcaDatabase
from .exceptions import OrcaException, OrcaNotFoundException
from .file_ingestor import (
    CSVIngestor,
    JSONIngestor,
    JSONLIngestor,
    ParquetIngestor,
    PickleIngestor,
)
from .hf_utils import HFAutoModelWrapper, HFDatasetIngestor
from .index_handle import IndexHandle
from .index_query import BatchedVectorScanResult, DefaultIndexQuery, VectorIndexQuery
from .orca_expr import ColumnHandle, OrcaExpr
from .orca_types import (
    BFloat16T,
    BoolT,
    DocumentT,
    Float16T,
    Float32T,
    Float64T,
    FloatT,
    ImageT,
    Int8T,
    Int16T,
    Int32T,
    Int64T,
    IntT,
    NumericTypeHandle,
    OrcaTypeHandle,
    TextT,
    UInt8T,
    UInt16T,
    UInt32T,
    UInt64T,
    VectorT,
)
from .table import TableHandle
from .temp_database import TemporaryDatabase, TemporaryTable


def set_credentials(*, api_key: str, secret_key: str, endpoint: Optional[str] = None):
    OrcaClient.set_credentials(api_key=api_key, secret_key=secret_key, endpoint=endpoint)


@with_default_database_method
def create_table(
    db,
    table_name: str,
    if_table_exists: TableCreateMode = TableCreateMode.ERROR_IF_TABLE_EXISTS,
    **columns: OrcaTypeHandle,
) -> TableHandle:
    """Create a table in the default database."""
    return db.create_table(table_name, if_table_exists, **columns)


@with_default_database_method
def get_table(db, table_name: str) -> TableHandle:
    """Get a table from the default database."""
    return db.get_table(table_name)


@with_default_database_method
def list_tables(db):
    """List tables in the default database."""
    return db.list_tables()


@with_default_database_method
def backup(db) -> tuple[str, str]:
    """Backup the default database."""
    return db.backup()


@with_default_database_method
def default_vectorize(db, text: str) -> list[float]:
    """Vectorize text using the default database."""
    return db.default_vectorize(text)


@with_default_database_method
def get_index(db, index_name: str):
    """Get an index from the default database."""
    return db.get_index(index_name)


@with_default_database_method
def create_vector_index(
    db,
    index_name: str,
    table_name: str,
    column: str,
    error_if_exists: bool = True,
):
    """Create a vector index for default db."""
    db.create_vector_index(index_name, table_name, column, error_if_exists)


@with_default_database_method
def create_document_index(
    db,
    index_name: str,
    table_name: str,
    column: str,
    error_if_exists: bool = True,
):
    """Create a document index for default db."""
    db.create_document_index(index_name, table_name, column, error_if_exists)


@with_default_database_method
def create_text_index(
    db,
    index_name: str,
    table_name: str,
    column: str,
    error_if_exists: bool = True,
):
    """Create a text index for default db."""
    db.create_text_index(index_name, table_name, column, error_if_exists)


@with_default_database_method
def create_btree_index(
    db,
    index_name: str,
    table_name: str,
    column: str,
    error_if_exists: bool = True,
):
    """Create a btree index for default db."""
    db.create_btree_index(index_name, table_name, column, error_if_exists)


@with_default_database_method
def drop_index(db, index_name: str, error_if_not_exists: bool = True):
    """Drop an index from the default database."""
    db.drop_index(index_name, error_if_not_exists)


@with_default_database_method
def drop_table(db, table_name: str, error_if_not_exists: bool = True):
    """Drop a table from the default database."""
    db.drop_table(table_name, error_if_not_exists)


@with_default_database_method
def search_memory(
    db,
    index_name: str,
    query: list[float],
    limit: int,
    columns: Optional[list[str]] = None,
):
    """Search memory for default db."""
    return db.search_memory(index_name, query, limit, columns)


@with_default_database_method
def scan_index(
    db,
    index_name: str,
    query: Any,
) -> DefaultIndexQuery:
    """Scan an index for default db."""
    return db.scan_index(index_name, query)


@with_default_database_method
def vector_scan_index(
    db,
    index_name: str,
    query: Any,
) -> VectorIndexQuery:
    """Scan a vector index for default db."""
    return db.vector_scan_index(index_name, query)


@with_default_database_method
def full_vector_memory_join(
    db,
    *,
    index_name: str,
    memory_index_name: str,
    num_memories: int,
    query_columns: list[str],
    page_index: int,
    page_size: int,
) -> dict[str, list[tuple[list[float], Any]]]:
    """Join a vector index with a memory index for default db."""
    return db.full_vector_memory_join(index_name, memory_index_name, num_memories, query_columns, page_index, page_size)


@with_default_database_method
def query(db, query: str, params: list[None | int | float | bytes | str] = []):
    """Execute a raw SQL query."""
    return db.query(query, params)


@with_default_database_method
def record_model_scores(db, run_ids: list[int] | int, scores: list[float] | float):
    """Record model scores in the default database."""
    db.record_model_scores(run_ids, scores)


@with_default_database_method
def record_model_input_output(db, run_ids: list[int] | int, inputs: list[Any] | Any, outputs: list[Any] | Any):
    """Record model inputs and outputs in the default database."""
    db.record_model_input_output(run_ids, inputs, outputs)
