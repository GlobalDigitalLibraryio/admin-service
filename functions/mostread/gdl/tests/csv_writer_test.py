import unittest

from ..csv_writer import CsvWriter


class CsvWriterTest(unittest.TestCase):
    @staticmethod
    def test_write_to_string_without_header():
        assert '''Donald,Duck\r\nDolly,Duck\r\n''' == CsvWriter().as_csv_string([["Donald", "Duck"], ["Dolly", "Duck"]])

    @staticmethod
    def test_write_to_string_with_header():
        assert '''First name,Last name\r\nDonald,Duck\r\nDolly,Duck\r\n''' == CsvWriter().as_csv_string([["Donald", "Duck"], ["Dolly", "Duck"]], ['First name', 'Last name'])