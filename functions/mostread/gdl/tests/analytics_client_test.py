from unittest import TestCase

from mock import Mock, patch

from ..analytics_client import AnalyticsClient


class AnalyticsClientTest(TestCase):
    @staticmethod
    def test_that_client_returns_report():
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

        analytics_mock = Mock()
        reports_mock = Mock()
        batch_get_mock = Mock()

        analytics_mock.reports.return_value = reports_mock
        reports_mock.batchGet.return_value = batch_get_mock
        batch_get_mock.execute.return_value = json_response

        with patch.object(AnalyticsClient, '_create_analytics', return_value=analytics_mock):
            client = AnalyticsClient("view_id", "credentials_json")
            response = client.get_most_read_books(2, 10)
            assert len(response) == 2
            assert response[0][0] == 2
            assert response[0][1] == 'Title 1'
            assert response[1][0] == 1
            assert response[1][1] == 'Title 2'

    @staticmethod
    def test_that_client_returns_none_on_error():
        analytics_mock = Mock()
        analytics_mock.reports.side_effect = RuntimeError('Something failed')

        with patch.object(AnalyticsClient, '_create_analytics', return_value=analytics_mock):
            client = AnalyticsClient("view_id", "credentials_json")
            response = client.get_most_read_books(2,10)
            assert response is None
