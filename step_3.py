"""
dapr run python3 state_store.py

- state - local redis
- pubsub - redis streams
- tracing - local zipkin

"""

from dapr.clients import DaprClient

from dapr.clients.grpc._request import (
    TransactionalStateOperation,
    TransactionOperationType,
)
from dapr.clients.grpc._state import StateItem
from context import WorkflowContext

from uuid import uuid4

import os

import asyncio
import aiohttp

async def make_request(url):
    print(f"making request to {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                print(await resp.text())

with WorkflowContext('step_3') as context:
    with DaprClient(address=context['dapr_address']) as d:
        storeName = "cosmosStateStore"
        key = "workingDirectory"

        longRunningURL = os.environ.get('longRunningURL')
        longRunningURLCode = os.environ.get('longRunningURLCode')

        loop = asyncio.get_event_loop()
        loop.run_until_complete(make_request(f"{longRunningURL}?code={longRunningURLCode}"))

        context['step_3_variable'] = f"Step_3_variable.value = {uuid4().hex}"
        print(context)

