import os
from pathlib import Path

all_components = ["AZUREKEYVAULT", "LOCALREDISSTATE", "AZURESB"]

# "azuresb",
# "cosmosstatestore",
# "kafka-binding",

component_dir = Path("components")
print(f"Component dir: {str(component_dir.absolute())}")
if not (component_dir.exists()):
    component_dir.mkdir()

for component in all_components:
    var_name = f"COMPONENT_{component}"
    component_value = os.environ.get(var_name)
    print(f"V - {var_name}: {component_value}")
    if component_value is not None:
        file_path = component_dir / f"{var_name}.yaml"
        print(f"Writing to {str(file_path.absolute())}")
        file_path.write_text(component_value)

workflow_cert = os.environ.get("WORKFLOWVAULTRBACCERT")
cert_txt_path = component_dir / "WORKFLOWVAULTRBACCERT.txt"
cert_txt_path.write_text(workflow_cert)
exec_command = (
    f"base64 -di {str(cert_txt_path)} > {str(component_dir)}/WORKFLOWVAULTRBACCERT.pfx"
)
print(f"Exec command: {exec_command}")
os.popen(exec_command)
