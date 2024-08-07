import unittest
import os
from datetime import datetime

from pkrcomponents.components.actions.action_move import ActionMove
from pkrcomponents.components.actions.street import Street
from pkrcomponents.components.cards.board import Board
from pkrcomponents.components.cards.combo import Combo
from pkrcomponents.components.players.player_hand_stats import PlayerHandStats
from pkrcomponents.components.players.players import Players
from pkrcomponents.components.players.position import Position
from pkrcomponents.components.tables.table import Table
from pkrcomponents.components.tournaments.buy_in import BuyIn
from pkrcomponents.components.tournaments.level import Level
from pkrcomponents.components.utils.exceptions import FullTableError
from pkrcomponents.converters.history_converter.local import LocalHandHistoryConverter
from pkrcomponents.converters.settings import BUCKET_NAME, DATA_DIR, TEST_DATA_DIR
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

