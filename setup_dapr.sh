#!/bin/sh

wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash
echo "::add-path::/home/runner/.dapr/bin"