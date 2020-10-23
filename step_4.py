from cloudevents.sdk.event import v1
from dapr.ext.grpc import App
import datetime
import os
import time

from uuid import uuid4

from dotenv import load_dotenv

load_dotenv()

step_name = "step_4"

app = App()

@app.subscribe(pubsub_name="azureservicebus", topic="longRunningTasks")
def longRunningTaskFinished(event: v1.Event) -> None:
    time.sleep(5)
    print(f"{step_name}: Long running task finished at {datetime.datetime.now().isoformat()}", flush=True)
    app.stop()


from context import WorkflowContext

with WorkflowContext(step_name) as context:
    print(f"{step_name}: Waiting for long running task to finish.", flush=True)
    
    app.run(50051)

    context.set_value(f"{step_name}: Random Value", uuid4().hex)
