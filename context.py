import datetime
from typing import Dict
import json
from json import dumps, loads
import datetime
import os

from dapr.clients.grpc.client import DaprClient

state_code = "39ed1967835243c693cd9e4723f2ac51"
storename = "redisstatestore"


class WorkflowContext(Dict):
    def __init__(self, step_name):
        dict.__init__(self)
        self["dapr_address"] = "localhost:20001"
        with DaprClient(address=self["dapr_address"]) as d:
            kv = d.get_state(storename, state_code)
            if kv.data == b"":
                kv.data = "{}"
            self.rehydrate(kv.data)

        self.start_step(step_name)

    def __getitem__(self, key):
        val = dict.__getitem__(self, key)
        return val

    def __setitem__(self, key, val):
        dict.__setitem__(self, key, val)

    def dehydrate(self):
        return dumps(self)

    def rehydrate(self, state_string):
        self.update(loads(state_string))

    def __enter__(self):
        return self

    def start_step(self, step_name):
        self["step_name"] = step_name
        self[self["step_name"]] = {}
        self[self["step_name"]]["start"] = datetime.datetime.now().isoformat()

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        with DaprClient(address=self["dapr_address"]) as d:
            self.end_step()
            kv = d.save_state(storename, state_code, self.dehydrate())
            os.popen(f"dapr stop --app-id {self['step_name']}")

    def end_step(self):
        self[self["step_name"]]["end"] = datetime.datetime.now().isoformat()
