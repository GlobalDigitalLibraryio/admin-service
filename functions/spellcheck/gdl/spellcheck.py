import logging
import json
from . import response


class Spellcheck:
    def __init__(self, bing_client):
        self.default_language = 'en'
        self.bing_client = bing_client
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)


    def main(self, event):
        text_to_check = self.get_text(event)
        language = self.get_language(event) or self.default_language
        spell_response = {'original': text_to_check if text_to_check else ""}

        if text_to_check:
            suggestion = self.bing_client.check_spelling(text_to_check, language)
            if suggestion:
                spell_response['suggestion'] = suggestion

        return response(body=json.dumps(spell_response))

    @staticmethod
    def get_text(event):
        q_params = event.get("queryStringParameters")
        return q_params.get("text") if q_params else None

    @staticmethod
    def get_language(event):
        q_params = event.get("queryStringParameters")
        return q_params.get("language") if q_params else None
