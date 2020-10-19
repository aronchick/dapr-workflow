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
if not (component_dir.exists()):
    component_dir.mkdir()

for component in all_components:
    var_name = f"COMPONENT_{component}"
    component_value = os.environ.get(var_name)
    if component_value is None:
        print(os.environ)
    file_path = component_dir / f"{var_name}.yaml"
    file_path.write_text(component_value)

os.popen("dapr init")
