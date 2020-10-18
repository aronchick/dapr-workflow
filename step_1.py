from dapr.clients import DaprClient
from uuid import uuid4

from context import WorkflowContext

with WorkflowContext("step_1") as context:
    with DaprClient(context["dapr_address"]) as d:
        key = "serviceKey"
        randomKey = "random"
        storeName = "azurekeyvault"

        resp = d.get_secret(store_name=storeName, key=key)

        print(
            f"I've executed step 1 with a very secret secret who's value is: {resp.secret[key]}"
        )
        context["step_1_variable"] = f"Step_1_variable.value = {uuid4().hex}"
