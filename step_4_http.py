import flask
from flask import request, jsonify
from flask_cors import CORS
import json
import sys

app = flask.Flask(__name__)
CORS(app)


@app.route("/dapr/subscribe", methods=["GET"])
def subscribe():
    subscriptions = [
        {
            "pubsubname": "azureservicebus",
            "topic": "longRunningTasks",
            "route": "longRunningTasksRoute",
        },
        {"pubsubname": "pubsub", "topic": "C", "route": "C"},
    ]
    return jsonify(subscriptions)


@app.route("/longRunningTasksRoute", methods=["POST"])
def longRunningTasksRoute_subscriber():
    print(f"longRunningTasksMessage: {request.json}", flush=True)
    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


app.run(port=4000)
