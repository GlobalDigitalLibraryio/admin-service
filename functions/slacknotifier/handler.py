import os
import time
import json
import boto3
import requests
from base64 import b64decode
from dateutil import parser

SLACK_CHANNEL = "#gdl-alarms"
SLACK_USER = "gdlbot"
SLACK_WEBHOOK_URL = boto3.client('kms').decrypt(CiphertextBlob=b64decode(os.environ['SLACK_WEBHOOK_URL']))['Plaintext'].decode()

def is_warmup(event):
    return event.get("source", "") == "serverless-plugin-warmup"

def main(event, context):
    if is_warmup(event):
        return "Warm"

    """
    Send Slack Message to Alarms Channel
    """

    sns = event["Records"][0]["Sns"]
    json_msg = json.loads(sns["Message"])

    if sns["Subject"]:
        message = sns["Subject"]
    else:
        message = sns["Message"]
    event_cond = json_msg["NewStateValue"]
    color_map = {
        "ALARM": "danger",
        "INSUFFICIENT_DATA": "warning",
    }
    emoji_map = {
        "ALARM": ":fire",
        "INSUFFICIENT_DATA": ":question:",
    }

    attachments = [{
        "fallback": json_msg,
        "message": json_msg,
        "color": color_map[event_cond],
        "fields": [{
            "title": "Alarm Metric",
            "value": json_msg["Trigger"]["MetricName"],
            "short": True
        }, {
            "title": "Status",
            "value": json_msg["NewStateValue"],
            "short": True
        }, {
            "title": "Function name",
            "value": json_msg["Trigger"]["Dimensions"][0]["value"],
            "short": False
        }, {
            "title": "Trigger",
            "value": json_msg["NewStateReason"],
            "short": False
        }]
    }]

    region = sns["TopicArn"].split(":")[3]
    topic_name = sns["TopicArn"].split(":")[-1]
    payload = {
        "icon_emoji": emoji_map[event_cond],
        "text": "AWS CloudWatch Notification",
        "channel": SLACK_CHANNEL,
        "username": SLACK_USER,
        "attachments": attachments
    }

    r = requests.post(SLACK_WEBHOOK_URL, json=payload)

    return r.status_code

