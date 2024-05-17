# pylint: disable=unused-import

from typing import Dict, Iterable, Optional, Type

import numpy as np
import pandas as pd
import pandera as pa
import pandera.typing


def get_dataset_type_schema(dataset_type: Type[pa.typing.DataFrame]) -> Type[pa.SchemaModel]:
    if not hasattr(dataset_type, '__args__'):
        raise ValueError(f'{dataset_type} is not a generic type')
    type_args = dataset_type.__args__
    if not type_args:
        raise ValueError(f'{dataset_type} has empty args')
    schema_type = dataset_type.__args__[0]
    if not issubclass(schema_type, pa.SchemaModel):
        raise ValueError(f'{dataset_type} is expected to have first type arg of panera.SchemaModel')
    return schema_type


def get_schema_dtypes(dataset_type: Type[pa.typing.DataFrame]) -> Dict[str, np.dtype]:
    schema_type = get_dataset_type_schema(dataset_type)

    dtypes = {k: v.dtype.type for k, v in schema_type.to_schema().columns.items()}
    return dtypes


def get_schema_columns(dataset_type: Type[pa.typing.DataFrame]) -> Iterable[str]:
    schema_type = get_dataset_type_schema(dataset_type)
    return schema_type.to_schema().columns.keys()


def get_schema_index_name(dataset_type: Type[pa.typing.DataFrame]) -> Optional[str]:
    schema_type = get_dataset_type_schema(dataset_type)
    index = schema_type.to_schema().index
    result = None if (index is None) else index.name
    return result


def get_schema_index_dtype(dataset_type: Type[pa.typing.DataFrame]) -> Optional[np.dtype]:
    schema_type = get_dataset_type_schema(dataset_type)
    index = schema_type.to_schema().index
    result = None if (index is None) else index.dtype.type
    return result


def create_schema_empty_data_frame(dataset_type: Type[pa.typing.DataFrame]) -> pd.DataFrame:
    columns_dtypes = get_schema_dtypes(dataset_type)
    index_name = get_schema_index_name(dataset_type)
    index_dtype = get_schema_index_dtype(dataset_type)
    if (index_name is None) and (index_dtype is None):
        index = None
    else:
        index = pd.Series(dtype=index_dtype, name=index_name)
    columns_series = {c: pd.Series(dtype=t) for c, t in columns_dtypes.items()}

    return pd.DataFrame(columns_series, index=index)
