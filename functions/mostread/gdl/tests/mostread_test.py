import unittest
import pytest

from mock import Mock

from ..mostread import MostRead


class MostReadTest(unittest.TestCase):
    def setUp(self):
        self.csv_writer_mock = Mock()
        self.analytics_client_mock = Mock()

        self.most_read = MostRead(self.analytics_client_mock, self.csv_writer_mock)

    def test_response_200_default_params(self):
        expected_csv_content = "Count, Title\n1,Title1"

        self.analytics_client_mock.get_most_read_books.return_value = [[]]
        self.csv_writer_mock.as_csv_string.return_value = expected_csv_content
        response = self.most_read.main(event={})

        assert response['statusCode'] == 200
        assert response['headers']['Content-Type'] == 'text/csv'
        assert response['body'] == expected_csv_content

    def test_response_200_all_params_specified(self):
        expected_csv_content = "Count, Title\n1,Title1"

        self.analytics_client_mock.get_most_read_books.return_value = [[]]
        self.csv_writer_mock.as_csv_string.return_value = expected_csv_content
        response = self.most_read.main(event={'queryStringParameters': {'days': 100, 'n': 100}})

        self.analytics_client_mock.get_most_read_books.assert_called_with(100, 100)
        assert response['statusCode'] == 200
        assert response['headers']['Content-Type'] == 'text/csv'
        assert response['body'] == expected_csv_content

    def test_response_200_one_of_two_params_specified(self):
        expected_csv_content = "Count, Title\n1,Title1"

        self.analytics_client_mock.get_most_read_books.return_value = [[]]
        self.csv_writer_mock.as_csv_string.return_value = expected_csv_content
        response = self.most_read.main(event={'queryStringParameters': {'n': 100}})

        self.analytics_client_mock.get_most_read_books.assert_called_with(100, MostRead.DEFAULT_DAYS)
        assert response['statusCode'] == 200
        assert response['headers']['Content-Type'] == 'text/csv'
        assert response['body'] == expected_csv_content

    def test_response_500(self):
        self.analytics_client_mock.get_most_read_books.return_value = []
        response = self.most_read.main(event={})

        assert response['statusCode'] == 500
        assert response['body'] == "Could not fetch analytics data"

    @staticmethod
    def test_get_n():
        def verify_exception(value):
            with pytest.raises(ValueError, match=r'n must be an integer between {} and {}'.format(MostRead.MIN_NUM_ITEMS, MostRead.MAX_NUM_ITEMS)):
                MostRead.get_n({'n': value})

        assert MostRead.get_n(None) == MostRead.DEFAULT_NUM_ITEMS
        assert MostRead.get_n({}) == MostRead.DEFAULT_NUM_ITEMS
        assert MostRead.get_n({'n': MostRead.MAX_NUM_ITEMS}) == MostRead.MAX_NUM_ITEMS
        assert MostRead.get_n({'n': MostRead.MIN_NUM_ITEMS}) == MostRead.MIN_NUM_ITEMS
        assert MostRead.get_n({'n': MostRead.MAX_NUM_ITEMS - 1}) == MostRead.MAX_NUM_ITEMS - 1
        assert MostRead.get_n({'n': MostRead.MIN_NUM_ITEMS + 1}) == MostRead.MIN_NUM_ITEMS + 1

        verify_exception(MostRead.MAX_NUM_ITEMS + 1)
        verify_exception(MostRead.MIN_NUM_ITEMS - 1)

    @staticmethod
    def test_get_days():
        def verify_exception(value):
            with pytest.raises(ValueError, match=r'days must be an integer between {} and {}'.format(MostRead.MIN_DAYS, MostRead.MAX_DAYS)):
                MostRead.get_days({'days': value})

        assert MostRead.get_days(None) == MostRead.DEFAULT_DAYS
        assert MostRead.get_days({}) == MostRead.DEFAULT_DAYS
        assert MostRead.get_days({'days': MostRead.MIN_DAYS}) == MostRead.MIN_DAYS
        assert MostRead.get_days({'days': MostRead.MAX_DAYS}) == MostRead.MAX_DAYS
        assert MostRead.get_days({'days': MostRead.MIN_DAYS + 1}) == MostRead.MIN_DAYS + 1
        assert MostRead.get_days({'days': MostRead.MAX_DAYS - 1}) == MostRead.MAX_DAYS - 1

        verify_exception(MostRead.MAX_DAYS + 1)
        verify_exception(MostRead.MIN_DAYS - 1)



