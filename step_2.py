"""
dapr run python3 state_store.py
"""

import contextlib
from datetime import datetime
from context import WorkflowContext
from os import urandom
from dapr.clients import DaprClient

from dapr.clients.grpc._request import (
    TransactionalStateOperation,
    TransactionOperationType,
)
from dapr.clients.grpc._state import StateItem
from random import randint
import asyncio

from uuid import uuid4

key_name = "key_name"
state_store = "redisstatestore"

async def execute_step(daprClient, storeName, key, value):
    await asyncio.sleep(randint(1,2))

    # Save single state.
    daprClient.save_state(
        store_name=storeName,
        key=key,
        value=value
    )
    print(f"Wrote {{ {key_name}: {value} }} to DB at {datetime.now().isoformat()}")

def two_parallel_jobs(daprClient, storename):
    tasks =  []
    loop = asyncio.new_event_loop()

    tasks.append(loop.create_task(execute_step(daprClient, storename, key_name, "value-1000")))
    tasks.append(loop.create_task(execute_step(daprClient, storename, key_name, "value-2000")))

    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


with WorkflowContext('step_2') as context:
    with DaprClient(address="localhost:20001") as d:
        two_parallel_jobs(d, state_store)

        a = d.get_state(state_store, key_name)
        print(f"the final value of the data is: {a.data}")

        context['step_2_variable'] = f"Step_2_variable.value = {uuid4().hex}"

    print(context)