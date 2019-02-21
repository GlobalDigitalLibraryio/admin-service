import requests
import textwrap
from . import SpellReport

class BingClient:

    BING_MAX_TEXT_SIZE = 65

    def __init__(self, api_key, api_endpoint, max_size_string):
        self.api_key = api_key
        self.api_endpoint = api_endpoint
        self.max_size_string = max_size_string

    def get_report_for_text(self, text, lang_iso639):
        response = requests.post(self.api_endpoint, params={
            'mode': 'spell',
            'text': text,
            'setLang': lang_iso639,
            'mkt': lang_iso639}, headers={'Ocp-Apim-Subscription-Key': self.api_key, 'Pragma': 'no-cache'})
        response.raise_for_status()
        response_json = response.json()
        report = SpellReport(text)

        corrected = text
        flagged_tokens = response_json.get('flaggedTokens')
        if flagged_tokens:
            offset_correction = 0
            for token in flagged_tokens:
                misspelled = token['token']
                offset = token['offset']
                suggestion = token['suggestions'][0]['suggestion']

                corrected_offset = offset - offset_correction
                end_offset = corrected_offset + len(misspelled)

                corrected = corrected[:corrected_offset] + suggestion + corrected[end_offset:]
                offset_correction = offset_correction + (len(misspelled) - len(suggestion))
                report.add_word_correction(misspelled, suggestion)

        report.add_suggestion(corrected)
        return report


    def check_spelling(self, text, lang_iso639):
        chunks = textwrap.wrap(text, self.max_size_string)
        reports = [self.get_report_for_text(chunk, lang_iso639) for chunk in chunks]

        all_corrections = []
        for report in reports:
            for item in report.corrections:
                all_corrections.append(item)

        report = SpellReport(text)
        report.add_suggestion(' '.join([x.suggestion for x in reports]))
        report.set_corrections(all_corrections)

        return report
