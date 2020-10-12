"""
dapr run python3 state_store.py
"""

from dapr.clients import DaprClient

from dapr.clients.grpc._request import (
    TransactionalStateOperation,
    TransactionOperationType,
)
from dapr.clients.grpc._state import StateItem

with DaprClient(address="localhost:20001") as d:
    storeName = "cosmosStateStore"

    key = "workingDirectory"

    # Get one state by key.
    working_directory = d.get_state(store_name=storeName, key=key).data
    print(f"Got value: {data}")

