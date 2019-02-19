import requests
import json

class BingClient:

    def __init__(self, api_key, api_endpoint):
        self.api_key = api_key
        self.api_endpoint = api_endpoint

    def check_spelling(self, text, lang_iso639):
        corrected = text


        response = requests.get(self.api_endpoint, params={
            'mode': 'spell',
            'text': text,
            'setLang': lang_iso639}, headers={'Ocp-Apim-Subscription-Key': self.api_key})
        response.raise_for_status()

        json_resp = response.json()
        flagged_tokens = json_resp.get('flaggedTokens')
        if flagged_tokens:
            offset_correction = 0
            for token in flagged_tokens:
                misspelled = token['token']
                offset = token['offset']
                suggestion = sorted(token['suggestions'], key=lambda x: x['score'])[0]['suggestion']

                corrected_offset = offset - offset_correction
                end_offset = corrected_offset + len(misspelled)

                corrected = corrected[:corrected_offset] + suggestion + corrected[end_offset:]
                offset_correction = len(misspelled) - len(suggestion)

        return corrected if text != corrected else None
