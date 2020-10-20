#!/bin/sh

wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash
echo "/home/runner/.dapr/bin" >> $GITHUB_PATH