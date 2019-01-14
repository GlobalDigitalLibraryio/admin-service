import csv
import io


class CsvWriter:
    def __init__(self, delim=','):
        self.delimiter = delim

    def as_csv_string(self, item_list, header=None):
        out = io.BytesIO()
        writer = csv.writer(out, delimiter=self.delimiter)
        if header:
            writer.writerow(header)

        for item in item_list:
            writer.writerow(item)

        return out.getvalue()
