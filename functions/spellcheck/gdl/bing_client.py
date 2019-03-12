import requests
import textwrap
from . import SpellReport

class BingClient:

    BING_MAX_TEXT_SIZE = 65

    def __init__(self, api_key, api_endpoint, max_size_string):
        self.api_key = api_key
        self.api_endpoint = api_endpoint
        self.max_size_string = max_size_string

    def get_report_for_text(self, text, lang_iso639, pre_context=None, post_context=None):
        params = {
            'mode': 'spell',
            'text': text,
            'setLang': lang_iso639,
            'mkt': lang_iso639
        }

        if pre_context:
            params['preContextText'] = pre_context

        if post_context:
            params['postContextText'] = post_context

        response = requests.post(self.api_endpoint, params=params, headers={'Ocp-Apim-Subscription-Key': self.api_key, 'Pragma': 'no-cache'})
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
                most_accurate_suggestion = token['suggestions'][0]['suggestion']
                report.add_word_correction(misspelled, most_accurate_suggestion)

                corrected_offset = offset - offset_correction
                end_offset = corrected_offset + len(misspelled)

                corrected = corrected[:corrected_offset] + most_accurate_suggestion + corrected[end_offset:]
                offset_correction += len(misspelled) - len(most_accurate_suggestion)

        report.add_suggestion(corrected)
        return report


    def check_spelling(self, text, lang_iso639):
        chunks = textwrap.wrap(text, self.max_size_string)

        reports = []
        for i in range(0, len(chunks)):
            pre_index = i - 1
            post_index = i + 1

            pre_context = chunks[pre_index] if pre_index > -1 else None
            post_context = chunks[post_index] if post_index < len(chunks) - 1 else None
            reports.append(self.get_report_for_text(chunks[i], lang_iso639, pre_context, post_context))

        all_corrections = []
        for report in reports:
            for item in report.corrections:
                all_corrections.append(item)

        report = SpellReport(text)
        report.add_suggestion(' '.join([x.suggestion for x in reports]))
        report.set_corrections(all_corrections)

        return report
