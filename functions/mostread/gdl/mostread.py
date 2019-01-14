import logging
from . import response


class MostRead:
    DEFAULT_DAYS = 7
    DEFAULT_NUM_ITEMS = 20

    MIN_DAYS = 1
    MAX_DAYS = 365 * 10

    MIN_NUM_ITEMS = 1
    MAX_NUM_ITEMS = 1000

    def __init__(self, analytics_client, csv_writer):
        self.analytics_client = analytics_client
        self.csv_writer = csv_writer
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

    def main(self, event):
        q_params = event.get("queryStringParameters")
        try:
            n = self.get_n(q_params)
            days = self.get_days(q_params)
        except ValueError as ve:
            return response(status_code=400,
                            body=ve.message)

        most_read_books = self.analytics_client.get_most_read_books(n, days)

        if most_read_books:
            return response(
                headers={
                    "Content-Type": 'text/csv',
                    'Content-Disposition': 'inline; filename = "most-read-books.csv"'},
                body=self.csv_writer.as_csv_string(most_read_books, header=["Count", "Title"]))
        else:
            return response(
                status_code=500,
                body="Could not fetch analytics data")

    @staticmethod
    def get_days(q_params):
        requested_days = q_params.get("days") if q_params else None
        if requested_days is None:
            return MostRead.DEFAULT_DAYS

        try:
            assert MostRead.MIN_DAYS <= int(requested_days) <= MostRead.MAX_DAYS
            return requested_days
        except:
            raise ValueError('days must be an integer between {} and {}'.format(MostRead.MIN_DAYS, MostRead.MAX_DAYS))

    @staticmethod
    def get_n(q_params):
        requested_n = q_params.get("n") if q_params else None
        if requested_n is None:
            return MostRead.DEFAULT_NUM_ITEMS

        try:
            assert MostRead.MIN_NUM_ITEMS <= int(requested_n) <= MostRead.MAX_NUM_ITEMS
            return requested_n
        except:
            raise ValueError('n must be an integer between {} and {}'.format(MostRead.MIN_NUM_ITEMS, MostRead.MAX_NUM_ITEMS))

