# Setup
This demo requires that you set up three components - 
- Azure Service Bus
- Azure Key Vault
- Local Redis (this is available with dapr by default)

It also requires an endpoint to publish to, which an event to 'TOPICNAME'.

It also requires an environment variable named 'WORKFLOWVAULTRBACCERT' which is a base64 encoded cert necessary to interact with the key vault.

Hi Tim