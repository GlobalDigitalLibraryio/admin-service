import os
from base64 import b64decode

import boto3

from gdl.analytics_client import AnalyticsClient
from gdl.csv_writer import CsvWriter
from gdl.mostread import MostRead

ANALYTICS_CREDENTIALS = boto3.client('kms').decrypt(CiphertextBlob=b64decode(os.environ['ANALYTICS_CREDENTIALS']))['Plaintext']
ANALYTICS_VIEW_ID = boto3.client('kms').decrypt(CiphertextBlob=b64decode(os.environ['ANALYTICS_VIEW_ID']))['Plaintext']

analytics_client = AnalyticsClient(ANALYTICS_VIEW_ID, ANALYTICS_CREDENTIALS)
csv_writer = CsvWriter()
analytics = MostRead(analytics_client, csv_writer)


def is_warmup(event):
    return event.get('source', '') == "serverless-plugin-warmup"


def main(event, context):
    if is_warmup(event):
        return "Warm"

    return analytics.main(event)

