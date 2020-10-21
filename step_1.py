from dapr.clients import DaprClient
from uuid import uuid4

from context import WorkflowContext

with WorkflowContext("step_1") as context:
    with DaprClient(context["dapr_address"]) as d:
        key = "serviceKey"
        randomKey = "random"
        storeName = "azurekeyvault"

        resp = d.get_secret(store_name=storeName, key=key)

        context.set_value('step_1: Retrieved Secret', resp.secret[key])
        context.set_value("step_1: Random Value", uuid4().hex)
