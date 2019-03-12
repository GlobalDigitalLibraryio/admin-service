import json
import logging

from . import response

class Spellcheck:
    def __init__(self, bing_client):
        self.default_language = 'en-US'
        self.bing_client = bing_client
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

    def main(self, event):
        text_to_check = self.get_text(event)
        language = self.get_language(event) or self.default_language
        self.logger.info("TEXT = {}".format(text_to_check))
        self.logger.info("LANGUAGE = {}".format(language))
        spell_response = {'found_errors': False}

        if text_to_check:
            report = self.bing_client.check_spelling(text_to_check, language)
            spell_response['found_errors'] = report.contains_corrections()
            if report.contains_corrections():
                spell_response['original'] = text_to_check
                spell_response['suggestion'] = report.suggestion
                spell_response['corrections'] = report.corrections
        return response(body=json.dumps(spell_response))

    @staticmethod
    def get_params(event):
        if event.get("httpMethod") == 'POST':
            body = event.get("body")
            return json.loads(body) if body else {}
        elif event.get("httpMethod") == 'GET':
            q_params = event.get("queryStringParameters")
            return q_params if q_params else {}
        else:
            return {}

    @staticmethod
    def get_text(event):
        return Spellcheck.get_params(event).get("text")

    @staticmethod
    def get_language(event):
        return Spellcheck.get_params(event).get("language")
