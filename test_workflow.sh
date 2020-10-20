#!/bin/bash

python3 step_1.py
python3 step_2.py
python3 step_3.py
dapr run --app-id step_4 --app-protocol grpc --app-port 50051 -d ./components --log-level error python3 step_4.py