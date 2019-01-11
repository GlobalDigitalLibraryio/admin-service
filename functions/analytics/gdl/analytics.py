from . import response


class Analytics:
    DAYS = 7
    NUM_ITEMS = 20

    def __init__(self, analytics_client, csv_writer):
        self.analytics_client = analytics_client
        self.csv_writer = csv_writer

    def main(self, event):
        n = self.NUM_ITEMS
        days = self.DAYS
        if event.get("queryStringParameters"):
            q_params = event["queryStringParameters"]
            days = q_params.get("days") if q_params.get("days") else self.DAYS
            n = q_params.get("n") if q_params.get("n") else self.NUM_ITEMS

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

