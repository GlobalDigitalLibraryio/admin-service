import json
import logging

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


class AnalyticsClient:
    def __init__(self, analytics_view_id, analytics_credentials_json):
        self.analytics_view_id = analytics_view_id
        self.analytics_credentials_json = analytics_credentials_json
        self.analytics_scope = ['https://www.googleapis.com/auth/analytics.readonly']
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.ERROR)
        self.analytics = self._create_analytics(self.analytics_credentials_json, self.analytics_scope)

    @staticmethod
    def _create_analytics(analytics_credentials_json, analytics_scope):
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            json.loads(analytics_credentials_json, strict=False), analytics_scope)

        return build('analyticsreporting', 'v4', credentials=credentials)

    def _get_report(self, n, days):
        return self.analytics.reports().batchGet(
            body={
                "reportRequests":
                    [
                        {
                            "viewId": self.analytics_view_id,
                            "dateRanges":
                                [
                                    {
                                        "startDate": "{}daysAgo".format(days),
                                        "endDate": "1daysAgo"
                                    }
                                ],
                            "metrics":
                                [
                                    {
                                        "expression": "ga:totalEvents"
                                    }
                                ],
                            "orderBys":
                                [
                                    {"fieldName": "ga:totalEvents", "sortOrder": "DESCENDING"}
                                ],
                            "dimensions":
                                [
                                    {
                                        "name": "ga:eventAction"
                                    }
                                ],
                            "dimensionFilterClauses": [
                                {
                                    "filters": [
                                        {
                                            "dimensionName": "ga:eventAction",
                                            "operator": "EXACT",
                                            "expressions": ["Read"]
                                        }
                                    ]
                                }
                            ],
                            "pivots":
                                [
                                    {
                                        "dimensions":
                                            [
                                                {
                                                    "name": "ga:eventLabel"
                                                }
                                            ],
                                        "maxGroupCount": n,
                                        "startGroup": 0,
                                        "metrics":
                                            [
                                                {
                                                    "expression": "ga:totalEvents"
                                                }
                                            ]
                                    }
                                ]
                        }
                    ]
            }
        ).execute()

    def get_most_read_books(self, n, days):
        try:
            json_report = self._get_report(n, days)

            titles = json_report["reports"][0]["columnHeader"]["metricHeader"]["pivotHeaders"][0]["pivotHeaderEntries"]
            counts = json_report["reports"][0]["data"]["maximums"][0]["pivotValueRegions"][0]["values"]

            only_titles = [x["dimensionValues"][0] for x in titles]

            x = 0
            count_list = []
            for title in only_titles:
                count_list.append((counts[x], title))
                x += 1

            return count_list
        except Exception as e:
            self.logger.error("Could not export data from google analytics. Received error %s", e, exc_info=1)
            return None
