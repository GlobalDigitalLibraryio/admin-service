import unittest
import logging
from unittest.mock import patch

from gdl.analytics_client import AnalyticsClient


class AnalyticsClientTest(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)

    @patch.object(AnalyticsClient, '_create_analytics')
    @patch.object(AnalyticsClient, '_get_report')
    def test_that_client_returns_report(self, get_report_mock, create_analytics_mock):
        json_response = {
            'reports': [
                {
                    'columnHeader': {
                        'metricHeader': {
                            'pivotHeaders': [
                                {
                                    'pivotHeaderEntries': [
                                        {'dimensionValues': ['Title 1']},
                                        {'dimensionValues': ['Title 2']},
                                    ]
                                }
                            ]
                        }
                    },
                    'data': {
                        'maximums': [
                            {
                                'pivotValueRegions': [
                                    {'values': [2, 1]}
                                ]
                            }
                        ]
                    }
                }
            ]
        }

        create_analytics_mock.reports.return_value = get_report_mock
        get_report_mock.return_value = json_response

        client = AnalyticsClient("view_id", "credentials_json")
        response = client.get_most_read_books(2, 10)
        assert len(response) == 2
        assert response[0][0] == 2
        assert response[0][1] == 'Title 1'
        assert response[1][0] == 1
        assert response[1][1] == 'Title 2'



    @patch.object(AnalyticsClient, '_create_analytics')
    @patch.object(AnalyticsClient, '_get_report')
    def test_that_client_returns_none_on_error(self, get_report_mock, analytics_mock):
        analytics_mock.reports.return_value = get_report_mock
        get_report_mock.side_effect = RuntimeError("Something failed")

        client = AnalyticsClient("view_id", "credentials_json")

        response = client.get_most_read_books(2,10)
        assert response is None
        assert 1 == 1


if __name__ == '__main__':
    unittest.main()