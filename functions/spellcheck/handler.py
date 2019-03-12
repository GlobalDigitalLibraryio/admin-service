import os
import boto3
from base64 import b64decode
from gdl.spellcheck import Spellcheck
from gdl.bing_client import BingClient


BING_API_KEY = boto3.client('kms').decrypt(CiphertextBlob=b64decode(os.environ['BING_API_KEY']))['Plaintext'].decode()
BING_API_ENDPOINT = 'https://api.cognitive.microsoft.com/bing/v7.0/SpellCheck'
spellcheck = Spellcheck(BingClient(BING_API_KEY, BING_API_ENDPOINT, BingClient.BING_MAX_TEXT_SIZE))

def is_warmup(event):
    return event.get('source', '') == "serverless-plugin-warmup"


def main(event, context):
    if is_warmup(event):
        return "Warm"

    return spellcheck.main(event)

