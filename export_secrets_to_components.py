import os
from pathlib import Path

all_components = [
    "AZUREKEYVAULT",
]

# "azuresb",
# "cosmosstatestore",
# "kafka-binding",
# "localredisstate",

component_dir = Path("components")
print(f"Component dir: {component_dir}")
if not (component_dir.exists()):
    component_dir.mkdir()

for component in all_components:
    var_name = f"COMPONENT_{component}"
    component_value = os.environ.get(var_name)
    if component_value is None:
        print(os.environ)
        file_path = component_dir / f"{var_name}.yaml"
        file_path.write_text(component_value)

workflow_cert = os.environ.get('WORKFLOW_CERT')
cert_txt_path = component_dir / "workflow-cert.txt"
cert_txt_path.write_text(workflow_cert)
os.popen(f'base64 --decode {str(cert_txt_path)} > {str(component_dir)}/workflow-cert.pfx')


os.popen("dapr init")
