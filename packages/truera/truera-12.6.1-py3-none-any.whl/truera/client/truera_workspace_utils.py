from __future__ import annotations

from dataclasses import dataclass
import logging
import tempfile
from typing import Optional, TYPE_CHECKING
from urllib.parse import urlparse

if TYPE_CHECKING:
    import pandas as pd

from truera.protobuf.public.qoi_pb2 import \
    ExplanationAlgorithmType  # pylint: disable=no-name-in-module

REMOTE_ENV = "remote"
LOCAL_ENV = "local"


@dataclass(eq=True, frozen=True)
class ExplainerQiiCacheKey:
    score_type: str
    algorithm: ExplanationAlgorithmType


def format_connection_string(connection_string: str) -> str:
    '''Prepends https if no url scheme found in connection_string and removes any path in the url.'''
    if not urlparse(connection_string).scheme:
        connection_string = "https://" + connection_string

    # Keep only schema and netloc (exclude any path, params, query)
    url = urlparse(connection_string)
    connection_string = f"{url.scheme}://{url.netloc}"
    return urlparse(connection_string).geturl()


def sample_spark_dataframe(
    spark_dataframe,
    sample_count: int,
    sample_kind: str,
    seed: int,
    logger=None,
) -> pd.DataFrame:
    logger = logger if logger else logging.getLogger(__name__)
    total_count = spark_dataframe.count()
    sample_count = min(sample_count, total_count)
    if total_count == 0:
        raise ValueError("Provided Spark Dataframe is empty!")
    if sample_kind.lower() == "first":
        logger.info(
            f"Sampling first {sample_count} rows from PySpark DataFrame"
        )
        return spark_dataframe.limit(sample_count).toPandas()

    logger.info(
        f"Sampling approximately {sample_count} rows from PySpark DataFrame"
    )
    return spark_dataframe.sample(sample_count / total_count, seed).toPandas()


def create_temp_file_path(extension: Optional[str] = None) -> str:
    # In some scenarios, we cannot use NamedTemporaryFile
    # directly as it doesn't allow second open on Windows NT.
    # So we use NamedTemporaryFile to just create a name for us
    # and let it delete the file, but use the name later.
    with tempfile.NamedTemporaryFile(mode="w+") as file:
        file_name = file.name
        if extension:
            file_name += "." + extension
    return file_name
