from typing import Any, Optional

import orjson
import pandas
import torch
import tqdm
from orca_common import TableCreateMode
from transformers import AutoModel, AutoTokenizer

from orcalib.client import OrcaClient
from orcalib.exceptions import OrcaException
from orcalib.index_query import DefaultIndexQuery, VectorIndexQuery
from orcalib.orca_types import OrcaTypeHandle
from orcalib.table import TableHandle


class OrcaDatabase:
    name: str
    _default_instance = None

    def __init__(self, name: str):
        self.name = name
        OrcaClient.create_database(name)
        self.tables = OrcaClient.list_tables(name)
        self.tokenizer = None
        self.model = None

    def _load_model_and_tokenizer(self):
        if self.tokenizer is None or self.model is None:
            self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/multi-qa-mpnet-base-dot-v1")
            self.model = AutoModel.from_pretrained("sentence-transformers/multi-qa-mpnet-base-dot-v1")  # .to("cuda")
        return self.tokenizer, self.model

    def __contains__(self, table_name: str) -> bool:
        return table_name in self.tables

    def __getitem__(self, table_name: str) -> TableHandle:
        if table_name not in self.tables:
            raise ValueError(f"Table {table_name} not found in database {self.name}")
        return TableHandle(self.name, table_name)

    def get_table(self, table_name: str) -> TableHandle:
        return self.__getitem__(table_name)

    @classmethod
    def get_default_instance(cls):
        if cls._default_instance is None:
            cls._default_instance = cls("default")
        return cls._default_instance

    @staticmethod
    def list_databases():
        return OrcaClient.list_databases()

    @classmethod
    def is_server_up(cls) -> bool:
        try:
            cls.list_databases()
            return True
        except Exception:
            return False

    @classmethod
    def drop_database(cls, db: "str | OrcaDatabase", ignore_db_not_found: bool = False):
        """Drops a database by name or using the OrcaDatabase object"""
        db_name = db.name if isinstance(db, OrcaDatabase) else db
        OrcaClient.drop_database(db_name, ignore_db_not_found)

    @classmethod
    def exists(cls, db: "str | OrcaDatabase") -> bool:
        """Checks if a database exists by name or using the OrcaDatabase object"""
        db_name = db.name if isinstance(db, OrcaDatabase) else db
        return OrcaClient.database_exists(db_name)

    @staticmethod
    def restore(target_db_name: str, backup_name: str, checksum: str | None = None) -> "OrcaDatabase":
        """Restore a backup into a target database

        CAREFUL: this will overwrite the target database if it already exists

        :param target_db_name: name of database that backup will be restored into (will be created if it doesn't exist)
        :param backup_name: name of the backup to restore
        :param checksum: optionally the checksum for the backup
        :return: restored database
        """
        OrcaClient.restore_backup(target_db_name, backup_name, checksum=checksum)
        return OrcaDatabase(target_db_name)

    def list_tables(self):
        return OrcaClient.list_tables(self.name)

    def backup(self) -> tuple[str, str]:
        """Create a backup of the database

        :return: tuple containing name of the backup and checksum
        """
        res = OrcaClient.create_backup(self.name)
        return res["backup_name"], res["checksum"]

    @staticmethod
    def download_backup(backup_file_name: str):
        """Downloads the backup of the database
        :return: backed up file
        """
        return OrcaClient.download_backup(backup_file_name)

    @staticmethod
    def upload_backup(file_path: str):
        """Uploads tar file of the database
        :return: Upload response
        """
        return OrcaClient.upload_backup(file_path)

    @staticmethod
    def delete_backup(backup_file_name: str):
        """Delete backup file"""
        return OrcaClient.delete_backup(backup_file_name)

    def default_vectorize(self, text: str) -> list[float]:
        tokenizer, model = self._load_model_and_tokenizer()
        encoded_input = tokenizer(text, return_tensors="pt", padding="max_length", truncation=True)  # .to("cuda")
        output = model(**encoded_input)
        return output.pooler_output.tolist()[0]

    def create_table(
        self,
        table_name: str,
        if_table_exists: TableCreateMode = TableCreateMode.ERROR_IF_TABLE_EXISTS,
        **columns: OrcaTypeHandle,
    ) -> TableHandle:
        # We will deal with the case where the table already exists in server.
        self._create_table(table_name, if_table_exists, **columns)
        return self.get_table(table_name)

    def _create_table(
        self,
        table_name: str,
        if_table_exists: TableCreateMode,
        **columns: OrcaTypeHandle,
    ) -> TableHandle:
        table_schema = []
        for column_name, column_type in columns.items():
            table_schema.append(
                {
                    "name": column_name,
                    "dtype": column_type.full_name,
                    "notnull": column_type._notnull,
                    "unique": column_type._unique,
                }
            )
        OrcaClient.create_table(self.name, table_name, table_schema, if_table_exists)
        self.tables.append(table_name)
        return TableHandle(self.name, table_name)

    def _create_index(
        self,
        index_name: str,
        table_name: str,
        column: str,
        index_type: str,
        error_if_exists: bool = True,
    ):
        try:
            print(f"Creating index {index_name} of type {index_type} on table {table_name} with column {column}")
            OrcaClient.create_index(self.name, index_name, table_name, column, index_type)
        except OrcaException as e:
            if error_if_exists:
                raise e

    def get_index_status(self, index_name: str):
        try:
            return OrcaClient.get_index_status(db_name=self.name, index_name=index_name)
        except OrcaException as e:
            raise e

    def get_index(self, index_name: str):
        """Get a handle to an index by name"""
        return OrcaClient.get_index(self.name, index_name)

    def create_vector_index(
        self,
        index_name: str,
        table_name: str,
        column: str,
        error_if_exists: bool = True,
    ):
        self._create_index(index_name, table_name, column, "vector", error_if_exists)

    def create_document_index(
        self,
        index_name: str,
        table_name: str,
        column: str,
        error_if_exists: bool = True,
    ):
        self._create_index(index_name, table_name, column, "document", error_if_exists)

    def create_text_index(
        self,
        index_name: str,
        table_name: str,
        column: str,
        error_if_exists: bool = True,
    ):
        self._create_index(index_name, table_name, column, "text", error_if_exists)

    def create_btree_index(
        self,
        index_name: str,
        table_name: str,
        column: str,
        error_if_exists: bool = True,
    ):
        self._create_index(index_name, table_name, column, "btree", error_if_exists)

    def drop_index(self, index_name: str, error_if_not_exists: bool = True):
        try:
            OrcaClient.drop_index(self.name, index_name)
        except OrcaException as e:
            if error_if_not_exists:
                raise e

    def drop_table(self, table_name: str, error_if_not_exists: bool = True):
        OrcaClient.drop_table(self.name, table_name, error_if_not_exists)
        if table_name in self.tables:
            self.tables.remove(table_name)

    def search_memory(
        self,
        index_name: str,
        query: list[float],
        limit: int,
        columns: Optional[list[str]] = None,
    ):
        res = OrcaClient.scan_index(
            self,
            index_name,
            query,
            limit,
            columns,
        )
        return res

    def scan_index(
        self,
        index_name: str,
        query: Any,
    ) -> DefaultIndexQuery:
        return DefaultIndexQuery(
            db_name=self.name,
            primary_table=self._get_index_table(index_name),
            index=index_name,
            index_query=query,
        )

    def vector_scan_index(
        self,
        index_name: str,
        query: Any,
    ) -> VectorIndexQuery:
        return VectorIndexQuery(
            db_name=self.name,
            primary_table=self._get_index_table(index_name),
            index=index_name,
            index_query=query,
        )

    def full_vector_memory_join(
        self,
        *,
        index_name: str,
        memory_index_name: str,
        num_memories: int,
        query_columns: list[str],
        page_index: int,
        page_size: int,
    ) -> dict[str, list[tuple[list[float], Any]]]:
        res = OrcaClient.full_vector_memory_join(
            db_name=self.name,
            index_name=index_name,
            memory_index_name=memory_index_name,
            num_memories=num_memories,
            query_columns=query_columns,
            page_index=page_index,
            page_size=page_size,
        )

        return orjson.loads(res.text)

    def _get_index_values(self, index_name: str) -> dict[int, list[float]]:
        res = OrcaClient.get_index_values(self.name, index_name).json()
        return {int(k): v for k, v in res.items()}

    def _get_index_values_paginated(
        self,
        index_name: str,
        page_size: int = 1000,
    ) -> dict[int, list[float]]:
        page_index = 0

        result = {}

        res = OrcaClient.get_index_values_paginated(
            self.name, index_name, page_index=page_index, page_size=page_size
        ).json()

        num_pages = res["num_pages"]

        for v in res["items"]:
            result[int(v[0])] = v[1]

        if num_pages > 1:
            print(f"Fetching vectors for index {index_name} ({num_pages} pages)")

            for page_index in tqdm.tqdm(range(1, num_pages)):
                res = OrcaClient.get_index_values_paginated(
                    self.name, index_name, page_index=page_index, page_size=page_size
                ).json()

                for v in res["items"]:
                    result[int(v[0])] = v[1]

        print(f"Finished fetching vectors for index {index_name} ({num_pages} pages)")

        return result

    def _get_index_table(self, index_name: str):
        return TableHandle(self.name, OrcaClient.get_index_table(self.name, index_name).json())

    def memory_layer(self, index_name: str) -> torch.nn.Module:
        return torch.nn.Sequential(
            torch.nn.Linear(768, 768),
            torch.nn.ReLU(),
            torch.nn.Linear(768, 768),
            torch.nn.ReLU(),
            torch.nn.Linear(768, 768),
            torch.nn.ReLU(),
            torch.nn.Linear(768, 768),
        )

    def wrap_hf_model(self, index_name: str, model_name: str):
        pass

    def query(self, query: str, params: list[None | int | float | bytes | str] = []):
        """Send a read query to the database

        This cannot be used for inserting, updating, or deleting data.
        :param query: SQL query to run
        :param params: optional values to pass to a parametrized query
        """
        df = pandas.DataFrame(OrcaClient.run_sql(self.name, query, params))
        return df

    def record_model_scores(self, run_ids: list[int] | int, scores: list[float] | float):
        if isinstance(run_ids, int):
            run_ids = [run_ids]
            assert isinstance(scores, float), "Only a single score is allowed if a single run_id is provided"
            scores = [scores]
        assert isinstance(scores, list)
        OrcaClient.record_model_scores(self.name, run_ids, scores)

    def record_model_input_output(self, run_ids: list[int] | int, inputs: list[Any] | Any, outputs: list[Any] | Any):
        if isinstance(run_ids, int):
            run_ids = [run_ids]
            assert not isinstance(inputs, list) and not isinstance(
                outputs, list
            ), "Only a single input/output is allowed if a single run_id is provided"
            inputs = [inputs]
            outputs = [outputs]
        assert isinstance(inputs, list) and isinstance(outputs, list)
        OrcaClient.record_model_input_output(self.name, run_ids, inputs, outputs)

    def __str__(self):
        return f"OrcaDatabase({self.name}) - Tables: {', '.join(self.tables)}"

    def __repr__(self):
        return self.__str__()


def with_default_database_method(method):
    def wrapper(*args, **kwargs):
        default_database = OrcaDatabase.get_default_instance()
        return method(default_database, *args, **kwargs)

    return wrapper
