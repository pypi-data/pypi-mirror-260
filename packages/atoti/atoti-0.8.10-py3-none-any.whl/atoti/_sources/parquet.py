from __future__ import annotations

from collections.abc import Mapping, Set as AbstractSet
from typing import Optional

from atoti_core import Constant, DataType, PathLike, TableIdentifier
from pydantic import RootModel
from typing_extensions import override

from .._path_utils import to_absolute_path
from ..client_side_encryption_config import ClientSideEncryptionConfig
from .data_source import DataSource, InferTypes, LoadDataIntoTable


def create_parquet_params(
    path: PathLike,
    /,
    *,
    pattern: Optional[str],
    columns: Mapping[str, str],
    client_side_encryption: Optional[ClientSideEncryptionConfig],
) -> dict[str, object]:
    return {
        "absolutePath": to_absolute_path(path),
        "globPattern": pattern,
        "columns": columns,
        "clientSideEncryptionConfig": RootModel[type(client_side_encryption)](  # type: ignore[misc]
            client_side_encryption
        ).model_dump()
        if client_side_encryption is not None
        else None,
    }


class ParquetDataSource(DataSource):
    def __init__(
        self,
        *,
        infer_types: InferTypes,
        load_data_into_table: LoadDataIntoTable,
    ) -> None:
        super().__init__(load_data_into_table=load_data_into_table)

        self._infer_types = infer_types

    @property
    @override
    def key(self) -> str:
        return "PARQUET"

    def infer_parquet_types(
        self,
        path: PathLike,
        /,
        *,
        keys: AbstractSet[str],
        pattern: Optional[str],
        client_side_encryption: Optional[ClientSideEncryptionConfig],
        columns: Mapping[str, str],
        default_values: Mapping[str, Optional[Constant]],
    ) -> dict[str, DataType]:
        return self._infer_types(
            self.key,
            create_parquet_params(
                path,
                pattern=pattern,
                columns=columns,
                client_side_encryption=client_side_encryption,
            ),
            keys=keys,
            default_values=default_values,
        )

    def load_parquet_into_table(
        self,
        identifier: TableIdentifier,
        path: PathLike,
        /,
        *,
        columns: Mapping[str, str],
        scenario_name: str,
        pattern: Optional[str] = None,
        client_side_encryption: Optional[ClientSideEncryptionConfig] = None,
    ) -> None:
        self.load_data_into_table(
            identifier,
            create_parquet_params(
                path,
                pattern=pattern,
                columns=columns,
                client_side_encryption=client_side_encryption,
            ),
            scenario_name=scenario_name,
        )
