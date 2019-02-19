# coding=utf-8
import unittest
import json

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
        assert body['original'] == ""

    def test_response_200_correct_spelling(self):
        self.bing_client_mock.check_spelling.return_value = None
        text_to_check = 'hello'
        response = self.spellcheck.main(event={'queryStringParameters': {'text': text_to_check}})
        body = json.loads(response['body'])
        assert response['statusCode'] == 200
        assert body['original'] == text_to_check
        assert body.get('suggestion') is None


if __name__ == '__main__':
    unittest.main()
