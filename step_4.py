from cloudevents.sdk.event import v1
from dapr.ext.grpc import App
import datetime
import os
import time

from uuid import uuid4

from dotenv import load_dotenv

load_dotenv()

app = App()

@app.subscribe(pubsub_name="azureservicebus", topic="longRunningTasks")
def longRunningTaskFinished(event: v1.Event) -> None:
    time.sleep(5)
    print(f"Long running task finished at {datetime.datetime.now().isoformat()}", flush=True)
    app.stop()


from context import WorkflowContext

with WorkflowContext("step_4") as context:
    print("Waiting for long running task to finish.", flush=True)
    
    app.run(50051)

    context["step_4_variable"] = f"Step_4_variable.value = {uuid4().hex}"