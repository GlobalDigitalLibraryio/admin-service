import unittest

from mock import Mock

from ..analytics import Analytics


class AnalyticsTest(unittest.TestCase):
    def setUp(self):
        self.csv_writer_mock = Mock()
        self.analytics_client_mock = Mock()

        self.analytics = Analytics(self.analytics_client_mock, self.csv_writer_mock)

    def test_response_200_default_params(self):
        expected_csv_content = "Count, Title\n1,Title1"

        self.analytics_client_mock.get_most_read_books.return_value = [[]]
        self.csv_writer_mock.as_csv_string.return_value = expected_csv_content
        response = self.analytics.main(event={})

        assert response['statusCode'] == 200
        assert response['headers']['Content-Type'] == 'text/csv'
        assert response['body'] == expected_csv_content

    def test_response_200_all_params_specified(self):
        expected_csv_content = "Count, Title\n1,Title1"

        self.analytics_client_mock.get_most_read_books.return_value = [[]]
        self.csv_writer_mock.as_csv_string.return_value = expected_csv_content
        response = self.analytics.main(event={'queryStringParameters': {'days': 100, 'n': 100}})

        self.analytics_client_mock.get_most_read_books.assert_called_with(100, 100)
        assert response['statusCode'] == 200
        assert response['headers']['Content-Type'] == 'text/csv'
        assert response['body'] == expected_csv_content

    def test_response_200_one_of_two_params_specified(self):
        expected_csv_content = "Count, Title\n1,Title1"

        self.analytics_client_mock.get_most_read_books.return_value = [[]]
        self.csv_writer_mock.as_csv_string.return_value = expected_csv_content
        response = self.analytics.main(event={'queryStringParameters': {'n': 100}})

        self.analytics_client_mock.get_most_read_books.assert_called_with(100, Analytics.DAYS)
        assert response['statusCode'] == 200
        assert response['headers']['Content-Type'] == 'text/csv'
        assert response['body'] == expected_csv_content

    def test_response_500(self):
        self.analytics_client_mock.get_most_read_books.return_value = []
        response = self.analytics.main(event={})

        assert response['statusCode'] == 500
        assert response['body'] == "Could not fetch analytics data"
