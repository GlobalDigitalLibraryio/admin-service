import unittest
import requests_mock
import json
from gdl.bing_client import BingClient


class BingClientTestCase(unittest.TestCase):

    def setUp(self):
        self.api_key = '23'
        self.api_endpoint = 'http://www.mock.com'
        self.client = BingClient(self.api_key, self.api_endpoint)

    @requests_mock.mock()
    def test_no_spelling_errors(self, req_mock):
        api_endpoint = 'http://www.mock.com'
        api_key = '23'
        req_mock.get(api_endpoint, text='{}')

        client = BingClient(api_key, api_endpoint)
        assert client.check_spelling("Heisann", 'en') is None

    @requests_mock.mock()
    def test_one_spelling_error(self, req_mock):
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
        req_mock.get(self.api_endpoint, text=json.dumps(response_json))
        assert self.client.check_spelling('My nema is GDL', 'en') == 'My name is GDL'

    @requests_mock.mock()
    def test_multiple_spelling_errors(self, req_mock):
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
        req_mock.get(self.api_endpoint, text=json.dumps(response_json))
        assert self.client.check_spelling('My nema is Donald and I lve hambrugers', 'en') == 'My name is Donald and I love hamburgers'


if __name__ == '__main__':
    unittest.main()
