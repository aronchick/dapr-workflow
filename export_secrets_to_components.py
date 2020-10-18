import os

all_components = [
    "AZUREKEYVAULT",
]

    # "azuresb",
    # "cosmosstatestore",
    # "kafka-binding",
    # "localredisstate",

for component in all_components:
    component_value = os.environ.get(f"COMPONENT_{component}")

cert_name = 'workflow-cert'
os.popen(f'az keyvault secret download --vault-name workflow-vault --name {cert_name} --file {cert_name}-export.txt')
os.popen(f'base64 --decode {cert_name}.txt > components/{cert_name}.pfx')