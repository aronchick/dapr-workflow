#!/bin/sh

conda install pip setuptools wheel
wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash
dapr init -s
echo "::add-path::/home/runner/.dapr/bin"
rm  .dapr/components/statestore.yaml 
echo "$DAPR_REDIS_CONFIG" > .dapr/components/statestore.yaml
