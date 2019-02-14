# coding=utf-8
import unittest
import json

from gdl.spellcheck import Spellcheck


class SpellCheckTestCase(unittest.TestCase):

    def setUp(self):
        self.spellcheck = Spellcheck()

    def test_response_200_no_query_params(self):
        response = self.spellcheck.main(event={})

        body = json.loads(response['body'])
        assert response['statusCode'] == 200
        assert body['original'] == ""

    def test_response_200_correct_spelling(self):
        text_to_check = 'hello'
        response = self.spellcheck.main(event={'queryStringParameters': {'text': text_to_check}})
        body = json.loads(response['body'])
        assert response['statusCode'] == 200
        assert body['original'] == text_to_check
        assert body['suggestion'] == text_to_check


if __name__ == '__main__':
    unittest.main()
