# coding=utf-8
import unittest
import json

from gdl import SpellReport
from gdl.spellcheck import Spellcheck
from unittest.mock import Mock

class SpellCheckTestCase(unittest.TestCase):

    def setUp(self):
        self.bing_client_mock = Mock()
        self.spellcheck = Spellcheck(self.bing_client_mock)

    def test_response_200_no_query_params(self):
        response = self.spellcheck.main(event={})
        body = json.loads(response['body'])
        assert response['statusCode'] == 200
        assert body['found_errors'] == False

    def test_response_200_correct_spelling_get(self):
        text_to_check = 'hello'
        self.bing_client_mock.check_spelling.return_value = SpellReport(text_to_check)
        response = self.spellcheck.main(event={'httpMethod':'GET', 'queryStringParameters': {'text': text_to_check}})
        body = json.loads(response['body'])
        assert response['statusCode'] == 200
        assert body['found_errors'] == False

    def test_response_200_correct_spelling_post(self):
        text_to_check = 'hello'
        self.bing_client_mock.check_spelling.return_value = SpellReport(text_to_check)
        response = self.spellcheck.main(event={'httpMethod': 'POST', 'body': json.dumps({"text": text_to_check})})
        body = json.loads(response['body'])
        assert response['statusCode'] == 200
        assert body['found_errors'] == False

    def test_response_200_incorrect_spelling_get(self):
        text_to_check = "This contians a speling error"
        suggestion = "This contains a spelling error"
        corrections = [{"original": "contians", "correction": "contains"},{"original": "speling", "correction": "spelling"}]
        report = SpellReport(text_to_check)
        report.set_corrections(corrections)
        report.add_suggestion(suggestion)

        self.bing_client_mock.check_spelling.return_value = report
        response = self.spellcheck.main(event={'httpMethod': 'POST', 'body': json.dumps({"text": text_to_check})})
        body = json.loads(response['body'])
        assert response['statusCode'] == 200
        assert body['found_errors'] == True
        assert body['original'] == text_to_check
        assert body['suggestion'] == suggestion
        assert body['corrections'] == corrections

if __name__ == '__main__':
    unittest.main()
