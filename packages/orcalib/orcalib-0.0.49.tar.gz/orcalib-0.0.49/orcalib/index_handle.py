from typing import Any, Optional

from orca_common import ColumnName
from orcalib.orca_types import NumericTypeHandle, OrcaTypeHandle


class IndexHandle:
    """A handle to an index in an Orca database."""

    def __init__(
        self,
        name: str,
        db_name: str,
        table_name: str,
        column_name: ColumnName,
        column_type: OrcaTypeHandle,
        embedding_type: OrcaTypeHandle,
        index_type: str,
        artifact_columns: dict[ColumnName, str | OrcaTypeHandle],
    ):
        # Name of this index
        self.name = name
        # Database that this index belongs to
        self.db_name = db_name
        # Table that this index belongs to
        self.table_name = table_name
        # Name of the column that this index is built on
        self.column_name = column_name
        # Type of the column that this index is built on
        self.column_type = column_type
        # Type of the vector embedding used by this index (if any)
        self.embedding_type = embedding_type
        # Type of this index
        self.index_type = index_type
        # Artifact columns that are available from the index
        self.artifact_columns: dict[ColumnName, OrcaTypeHandle] = {
            column: (OrcaTypeHandle.from_string(column_type) if isinstance(column_type, str) else column_type)
            for column, column_type in artifact_columns.items()
        }

    @property
    def embedding_dim(self) -> Optional[int]:
        """Return the embedding dimension of this index (if any)."""
        if self.embedding_type is None or not isinstance(self.embedding_type, NumericTypeHandle):
            return None

        return self.embedding_type.length

    def scan(self, query: Any) -> "DefaultIndexQuery":  # noqa: F821
        """Scan the index for a given query."""
        from orcalib.index_query import DefaultIndexQuery

        return DefaultIndexQuery(
            db_name=self.name,
            primary_table=self._get_index_table(self.name),
            index=self.name,
            index_query=query,
        )

    def vector_scan(self, query: Any) -> "VectorIndexQuery":  # noqa: F821
        """Scan the index for a given query."""
        from orcalib.index_query import VectorIndexQuery

        return VectorIndexQuery(
            db_name=self.name,
            primary_table=self._get_index_table(self.name),
            index=self.name,
            index_query=query,
        )

    def get_status(self):
        from orcalib.client import OrcaClient

        return OrcaClient.get_index_status(self.db_name, self.name)

    def __str__(self):
        return f"{self.index_type} index: {self.name} on {self.db_name}.{self.table_name}.{self.column_name} ({self.column_type})"

    def __repr__(self):
        return str(self)
