import unittest
import requests_mock
from unittest.mock import patch
import json
from gdl.bing_client import BingClient
from gdl import SpellReport


class BingClientTestCase(unittest.TestCase):
    TEST_MAX_SIZE_STRING = 5

    def setUp(self):
        self.api_key = '23'
        self.api_endpoint = 'http://www.mock.com'
        self.client = BingClient(self.api_key, self.api_endpoint, BingClientTestCase.TEST_MAX_SIZE_STRING)

    @patch.object(BingClient, 'get_report_for_text')
    def test_check_spelling_only_one_chunk_no_errors(self, function_mock):
        function_mock.return_value = SpellReport("Hi")
        report = self.client.check_spelling("Hi", "en")
        assert report.contains_corrections() == False

    @patch.object(BingClient, 'get_report_for_text')
    def test_check_spelling_two_chunks_no_errors(self, function_mock):
        list_of_reports = [SpellReport("Next"), SpellReport("First")]

        def side_effect(a, b):
            return list_of_reports.pop()

        function_mock.side_effect = side_effect
        report = self.client.check_spelling("First Next", "en")
        assert report.suggestion == "First Next"
        assert report.contains_corrections() == False

    @patch.object(BingClient, 'get_report_for_text')
    def test_check_spelling_two_chunks_last_contains_error(self, function_mock):
        error_report = SpellReport("Nxet")
        error_report.add_word_correction("Nxet", "Next")
        error_report.add_suggestion("Next")
        list_of_reports = [error_report, SpellReport("First")]

        def side_effect(a, b):
            return list_of_reports.pop()

        function_mock.side_effect = side_effect
        report = self.client.check_spelling("First Nxet", "en")
        assert report.suggestion == "First Next"
        assert report.contains_corrections() == True
        assert report.corrections[0] == {"original": "Nxet", "correction": "Next"}

    @requests_mock.mock()
    def test_get_report_for_text_no_errors(self, req_mock):
        req_mock.post(self.api_endpoint, text='{}')
        report = self.client.check_spelling("Hello", "en")
        assert report.contains_corrections() == False
        assert report.suggestion == "Hello"

    @requests_mock.mock()
    def test_get_report_for_text_one_error(self, req_mock):
        response_json = {
            "flaggedTokens": [
                {
                    "offset": 3,
                    "token": "nema",
                    "type": "UnknownToken",
                    "suggestions": [
                        {
                            "suggestion": "name",
                            "score": 1
                        }
                    ]
                }
            ]
        }
        req_mock.post(self.api_endpoint, text=json.dumps(response_json))
        report = self.client.get_report_for_text('My nema is GDL', 'en')
        assert report.contains_corrections() == True
        assert report.corrections == [{"original": "nema", "correction": "name"}]
        assert report.suggestion == "My name is GDL"

    @requests_mock.mock()
    def test_get_report_for_text_multiple_spelling_errors(self, req_mock):
        response_json = {
            "flaggedTokens": [
                {
                    "offset": 3,
                    "token": "nema",
                    "type": "UnknownToken",
                    "suggestions": [
                        {
                            "suggestion": "name",
                            "score": 1
                        }
                    ]
                },
                {
                    "offset": 24,
                    "token": "lve",
                    "type": "UnknownToken",
                    "suggestions": [
                        {
                            "suggestion": "love",
                            "score": 1
                        }
                    ]
                },
                {
                    "offset": 28,
                    "token": "hambrugers",
                    "type": "UnknownToken",
                    "suggestions": [
                        {
                            "suggestion": "hamburgers",
                            "score": 1
                        }
                    ]
                }
            ]
        }
        req_mock.post(self.api_endpoint, text=json.dumps(response_json))
        report = self.client.get_report_for_text('My nema is Donald and I lve hambrugers', 'en')
        assert report.contains_corrections() == True
        assert report.corrections == [{"original": "nema", "correction": "name"}, {"original": "lve", "correction": "love"}, {"original": "hambrugers", "correction": "hamburgers"}]
        assert report.suggestion == 'My name is Donald and I love hamburgers'


if __name__ == '__main__':
    unittest.main()
