from json import load
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

from dotenv import load_dotenv

load_dotenv()

step_name = "step_3"
async def make_request(url):
    print(f"CALLER: Making REST call to long running external service at: {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                print(f"RESPONSE: {await resp.text()}")

    print(f"CALLER: Finished remote request.")


with WorkflowContext(step_name) as context:
    with DaprClient(address=context["dapr_address"]) as d:

        contentious_key_value = context.get("ContentiousKey")
        
        longRunningURL = os.environ.get("EXTERNAL_PIPELINE")
        longRunningURLCode = os.environ.get("EXTERNAL_PIPELINE_SHARED_SECRET")

        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            make_request(f"{longRunningURL}?code={longRunningURLCode}")
        )

        context.set_value(f"{step_name}: Random Value", uuid4().hex)

