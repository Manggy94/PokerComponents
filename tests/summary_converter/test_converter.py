import unittest
import os
from datetime import datetime
from pkrcomponents.components.tournaments.buy_in import BuyIn
from pkrcomponents.components.tournaments.level import Level
from pkrcomponents.components.tournaments.speed import TourSpeed
from pkrcomponents.converters.settings import BUCKET_NAME, DATA_DIR, TEST_DATA_DIR
from pkrcomponents.converters.summary_converter.local import LocalSummaryConverter

FILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "json_files")


class TestLocalSummaryConverter(unittest.TestCase):
    def setUp(self):
        self.history_path = os.path.join(FILES_DIR, 'example01.json')
        self.converter = LocalSummaryConverter(data_dir=DATA_DIR)
        self.converter.get_parsed_data(self.history_path)

    def test_list_parsed_summaries_keys(self):
        keys = self.converter.list_parsed_summaries_keys()
        self.assertIsInstance(keys, list)

    def test_get_tournament_name(self):
        self.converter.get_tournament_name()
        tournament_name = self.converter.tournament.name
        self.assertEqual(tournament_name, "GUERILLA")

    def test_get_registered_players(self):
        self.converter.get_registered_players()
        registered_players = self.converter.tournament.total_players
        self.assertEqual(registered_players, 2525)

    def test_get_buy_in(self):
        self.converter.get_buy_in()
        buy_in = self.converter.tournament.buy_in
        self.assertEqual(BuyIn(prize_pool=2.25, bounty=2.25, rake=0.5), buy_in)

    def test_get_tournament_speed(self):
        self.converter.get_tournament_speed()
        speed = self.converter.tournament.speed
        self.assertEqual(speed, TourSpeed.TURBO)

    def test_get_tournament_start_date(self):
        self.converter.get_tournament_start_date()
        start_date = self.converter.tournament.start_date
        date_format = "%d-%m-%Y %H:%M:%S"
        self.assertEqual(start_date, datetime.strptime("04-01-2023 17:30:01", date_format))

    def test_get_tournament(self):
        self.converter.get_tournament()
        self.assertEqual(self.converter.tournament.name, "GUERILLA")
        self.assertEqual(self.converter.tournament.id, "608341002")
        self.assertEqual(self.converter.tournament.level, Level(value=1, bb=200, ante=25))
        self.assertEqual(self.converter.tournament.buy_in, BuyIn(prize_pool=2.25, bounty=2.25, rake=0.5))

    def test_get_final_position(self):
        self.converter.get_final_position()
        final_position = self.converter.tournament.final_position
        self.assertEqual(final_position, 886)

    def test_get_amount_won(self):
        self.converter.get_amount_won()
        amount_won = self.converter.tournament.amount_won
        self.assertEqual(amount_won, 0.0)