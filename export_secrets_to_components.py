import os
from pathlib import Path

all_components = [
    "AZUREKEYVAULT",
]

    # "azuresb",
    # "cosmosstatestore",
    # "kafka-binding",
    # "localredisstate",

dapr_dir = Path('/home/runner/.dapr') 
if not (dapr_dir.exists()):
    dapr_dir.mkdir()

component_dir = dapr_dir / 'components'
if not (component_dir.exists()):
    component_dir.mkdir()

for component in all_components:
    var_name = f"COMPONENT_{component}"
    component_value = os.environ.get(var_name)
    file_path = component_dir / f"{var_name}.yaml"
    file_path.write_text(component_value)

cert_name = 'workflow-cert'
os.popen(f'az keyvault secret download --vault-name workflow-vault --name {cert_name} --file {cert_name}-export.txt')
os.popen(f'base64 --decode {cert_name}-export.txt > components/{cert_name}.pfx')

os.popen('dapr init')