"""Protocols defining the way corvic interacts with the platform."""

from corvic.system.client import Client
from corvic.system.op_graph_executor import OpGraphExecutor
from corvic.system.staging import StagingDB
from corvic.system.storage import (
    Blob,
    BlobClient,
    Bucket,
    DataKindManager,
    DataMisplacedError,
    StorageManager,
)

__all__ = [
    "Blob",
    "BlobClient",
    "Bucket",
    "Client",
    "DataKindManager",
    "DataMisplacedError",
    "OpGraphExecutor",
    "StagingDB",
    "StorageManager",
]
