from pandera import Field, SchemaModel
from pandera.typing import DataFrame, Series, Float32, Int32, Index

from panderaext.schema_helper import get_schema_columns


class TestDatasetSchema(SchemaModel):
    index: Index[Int32] = Field(unique=True)

    item_name: Series[str] = Field(nullable=False)
    price: Series[Float32] = Field(nullable=False)
    notes: Series[str] = Field(nullable=True)


TestDataset = DataFrame[TestDatasetSchema]


def test_it_gets_schema_columns():
    actual = list(get_schema_columns(TestDataset))
    expected = ['item_name', 'price', 'notes']
    assert actual == expected
