
from dapr.clients import DaprClient

# az keyvault secret set --name verySecret --vault-name workflow-vault --value "my VERY secret secret"

with DaprClient(address="localhost:20001") as d:
    key = 'serviceKey'
    randomKey = "random"
    storeName = 'azurekeyvault'

    resp = d.get_secret(store_name=storeName, key=key)

    print(f"I've executed step 1 with a very secret secret who's value is: {resp.secret[key]}")