import logging
import json
from . import response


class Spellcheck:
    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

    def check_spelling(self, text_to_check):
        return text_to_check

    def main(self, event):
        text_to_check = self.get_text(event)
        spell_response = {'original': text_to_check if text_to_check else ""}

        if text_to_check:
            suggestion = self.check_spelling(text_to_check)
            if suggestion:
                spell_response['suggestion'] = suggestion

        return response(body=json.dumps(spell_response))


    @staticmethod
    def get_text(event):
        q_params = event.get("queryStringParameters")
        return q_params.get("text") if q_params else None

