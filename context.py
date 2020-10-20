import datetime
from typing import Dict
import json
from json import dumps, loads
import datetime
import os
import uuid
from dotenv import load_dotenv

from dapr.clients.grpc.client import DaprClient

class WorkflowContext(Dict):
    __default_state_code = "39ed1967835243c693cd9e4723f2ac51"
    __default_storename = "redisstatestore"

    def __init__(self, step_name):
        load_dotenv()

        self.state_code = os.environ.get("GITHUB_SHA", self.__default_state_code)
        if os.environ.get("GITHUB_SHA") is not None:
            self.state_code = uuid.uuid4().hex
        self.storename = os.environ.get("STATE_STORE_NAME", self.__default_storename)
        
        dict.__init__(self)
        self["dapr_address"] = "localhost:20001"
        with DaprClient(address=self["dapr_address"]) as d:
            kv = d.get_state(self.storename, self.state_code)
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
        self["current_step_name"] = step_name
        
        if self.get('steps_executed', None) is None:
            self['steps_executed'] = []
        
        self['steps_executed'].append(step_name)

        if self.get('step_context', None) is None:
            self['step_context'] = {}
        
        self['step_context'][self["current_step_name"]] = {}
        self['step_context'][self["current_step_name"]]["start"] = datetime.datetime.now().isoformat()

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        with DaprClient(address=self["dapr_address"]) as d:
            self.end_step()
            kv = d.save_state(self.storename, self.state_code, self.dehydrate())
            os.popen(f'dapr stop --app-id {self["current_step_name"]}')
        
        print(self)

    def end_step(self):
        self['step_context'][self["current_step_name"]]["end"] = datetime.datetime.now().isoformat()

    def set_value(self, key, value):
        self['step_context'][self["current_step_name"]][key] = value