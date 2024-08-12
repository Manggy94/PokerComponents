import unittest
import os

from pkrcomponents.components.utils.exceptions import FullTableError
from pkrcomponents.converters.history_converter.local import LocalHandHistoryConverter
from pkrcomponents.converters.settings import DATA_DIR
from pkrcomponents.converters.utils.exceptions import HandConversionError

FILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "json_files")


class TestLocalHandHistoryConverter(unittest.TestCase):
    def setUp(self):
        self.converter = LocalHandHistoryConverter(data_dir=DATA_DIR)

    def test_convert_history1(self):
        history_path = os.path.join(FILES_DIR, 'example01.json')
        self.converter.get_parsed_data(history_path)
        with self.assertRaises(FullTableError):
            self.converter.convert_history(history_path)

    def test_convert_history2(self):
        history_path = os.path.join(FILES_DIR, 'example02.json')
        self.converter.get_parsed_data(history_path)
        with self.assertRaises(HandConversionError):
            self.converter.convert_history(history_path)

    def test_convert_history3(self):
        history_path = os.path.join(FILES_DIR, 'example03.json')
        self.converter.get_parsed_data(history_path)
        with self.assertRaises(HandConversionError):
            self.converter.convert_history(history_path)
