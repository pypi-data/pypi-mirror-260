from typing import Optional, Sequence

from truera.artifactrepo.utils.constants import SCHEMA_INPUT_COLUMN_LIMIT
from truera.protobuf.public.common.ingestion_schema_pb2 import Schema


def validate_data_collection_schema(schema: Schema) -> Sequence[ValueError]:
    """Returns list of validation errors of schema."""
    errors = []
    errors.extend(validate_column_limit(schema))
    errors.extend(validate_unique_columns(schema))
    return errors


def validate_column_limit(schema: Schema) -> Sequence[ValueError]:
    """Validate that the number of input columns is below limit"""
    if len(schema.input_columns) > SCHEMA_INPUT_COLUMN_LIMIT:
        return [
            ValueError(
                f"Number of input columns in data collection schema exceeds limit of {SCHEMA_INPUT_COLUMN_LIMIT}."
            )
        ]
    return []


def validate_unique_columns(schema: Schema) -> Sequence[ValueError]:
    """Validate that columns are unique"""
    errors = []
    column_kinds = {
        "id column": {schema.id_column_name},
        "timestamp column": {schema.timestamp_column_name},
        "tags column": {schema.tags_column_name},
        "input column": schema.input_columns,
        "output column": schema.output_columns,
        "label column": schema.label_columns,
        "extra column": schema.extra_columns,
    }
    column_set = {}
    for kind, columns in column_kinds.items():
        for column in columns:
            if column:
                if column in column_set:
                    errors.append(
                        ValueError(
                            f"Cannot set column '{column}' as {kind} as it is already set as {column_set[column]}."
                        )
                    )
                else:
                    column_set[column] = kind
    return errors
