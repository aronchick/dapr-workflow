from dapr.clients import DaprClient
from uuid import uuid4

from context import WorkflowContext

step_name = "step_1"

with WorkflowContext(step_name) as context:
    with DaprClient(context["dapr_address"]) as d:
        key = "servicekey"
        randomKey = "random"
        storeName = "azurekeyvault"

        print(f"Requesting secret from vault: serviceKeyRBACPassword")
        resp = d.get_secret(store_name=storeName, key=key)
        secret_value = resp.secret[key]
        print(f"Secret retrieved from vault: {secret_value}", flush=True)

        context.set_value(f'{step_name}: Retrieved Secret', secret_value)
        context.set_value(f"{step_name}: Random Value", uuid4().hex)
