import unittest
import os
from datetime import datetime
from pkrcomponents.components.cards.board import Board
from pkrcomponents.components.cards.combo import Combo
from pkrcomponents.components.players.hand_stats import HandStats
from pkrcomponents.components.players.players import Players
from pkrcomponents.components.players.position import Position
from pkrcomponents.components.tables.table import Table
from pkrcomponents.components.tournaments.buy_in import BuyIn
from pkrcomponents.components.tournaments.level import Level
from pkrcomponents.components.tournaments.speed import TourSpeed

from pkrcomponents.history_converter.converter import HandHistoryConverter
from pkrcomponents.history_converter.utils.exceptions import HandConversionError

FILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "json_files")


class TestHandHistoryConverter(unittest.TestCase):
    def setUp(self):
        self.history_path = os.path.join(FILES_DIR, 'example01.json')
        self.converter = HandHistoryConverter()
        self.converter.get_data(self.history_path)

    def test_get_data(self):
        self.assertIsInstance(self.converter.data, dict)

    def test_get_max_players(self):
        self.converter.get_max_players()
        self.assertEqual(self.converter.table.max_players, 6)

    def test_get_buy_in(self):
        buy_in = self.converter.get_buy_in()
        self.assertEqual(BuyIn(prize_pool=4.5, bounty=0, rake=0.5), buy_in)

    def test_get_level(self):
        level = self.converter.get_level()
        self.assertEqual(level.value, 1)
        self.assertEqual(level.bb, 200)
        self.assertEqual(level.sb, 100)
        self.assertEqual(level.ante, 25)

    def test_get_tournament_name(self):
        tournament_name = self.converter.get_tournament_name()
        self.assertEqual(tournament_name, "GUERILLA")

    def test_get_table_number(self):
        table_number = self.converter.get_table_number()
        self.assertEqual(table_number, "016")

    def test_get_hand_id(self):
        self.converter.get_hand_id()
        self.assertIsInstance(self.converter.table.hand_id, str)
        self.assertEqual(self.converter.table.hand_id, "2612804708405870609-6-1672853787")

    def test_get_datetime(self):
        self.converter.get_datetime()
        self.assertIsInstance(self.converter.table.hand_date, datetime)
        self.assertEqual(self.converter.table.hand_date, datetime(2023, 1, 4, 17, 36, 27))

    def test_get_game_type(self):
        game_type = self.converter.get_game_type()
        self.assertEqual(game_type, "Tournament")

    def test_get_tournament(self):
        self.converter.get_tournament()
        self.assertEqual(self.converter.table.tournament.name, "GUERILLA")
        self.assertEqual(self.converter.table.tournament.id, "608341002")
        self.assertEqual(self.converter.table.tournament.level, Level(value=1, bb=200, ante=25))
        self.assertEqual(self.converter.table.tournament.buy_in, BuyIn(prize_pool=4.5, bounty=0, rake=0.5))

    def test_get_button_seat(self):
        self.converter.get_button_seat()
        self.assertEqual(self.converter.table.players.bb_seat, 1)

    def test_get_players(self):
        self.converter.get_players()
        self.assertIsInstance(self.converter.table.players, Players)
        self.assertEqual(self.converter.table.players.len, 6)
        self.assertEqual(self.converter.table.players[1].name, "FrenchAAAA")
        self.assertEqual(self.converter.table.players[1].stack, 19575.0)
        self.assertEqual(self.converter.table.players[1].init_stack, 19575.0)
        self.assertEqual(self.converter.table.players[1].bounty, 2.25)
        self.assertEqual(self.converter.table.players[1].position, Position.UTG)

    def test_get_player(self):
        player_dict = self.converter.data.get("players").get("1")
        self.converter.get_player(player_dict)
        self.assertEqual(self.converter.table.players[1].name, "FrenchAAAA")
        self.assertEqual(self.converter.table.players[1].stack, 19575.0)
        self.assertEqual(self.converter.table.players[1].init_stack, 19575.0)
        self.assertEqual(self.converter.table.players[1].bounty, 2.25)

    def test_get_hero(self):
        self.converter.get_players()
        self.converter.get_hero()
        hero = self.converter.table.players["manggy94"]
        self.assertTrue(hero.is_hero)
        self.assertEqual(self.converter.table.hero_combo, Combo("5h2c"))

    def test_get_postings(self):
        self.converter.get_tournament()
        self.converter.get_players()
        self.converter.get_postings()
        self.assertEqual(self.converter.table.pot_value, 450)

    def test_get_actions(self):
        self.converter.get_tournament()
        self.converter.get_players()
        self.converter.get_postings()
        self.converter.get_actions()
        self.assertEqual(self.converter.table.pot_value, 7575.0)

    def test_get_tournament_speed(self):
        speed = self.converter.get_tournament_speed()
        self.assertEqual(speed, TourSpeed.TURBO)

    def test_get_registered_players(self):
        registered_players = self.converter.get_registered_players()
        self.assertEqual(registered_players, 2525)

    def test_get_tournament_start_date(self):
        start_date = self.converter.get_tournament_start_date()
        date_format = "%d-%m-%Y %H:%M:%S"
        self.assertEqual(start_date, datetime.strptime("04-01-2023 17:30:01", date_format))

    def test_convert_history(self):
        table = self.converter.convert_history(self.history_path)
        self.assertEqual(table.pot_value, 0.0)
        self.assertIsInstance(table, Table)
        hero_player = table.players["manggy94"]
        self.assertTrue(hero_player.is_hero)
        hero_stats = hero_player.hand_stats
        self.assertIsInstance(hero_stats, HandStats)
        # Preflop
        # Flags
        self.assertFalse(hero_stats.flag_vpip)
        self.assertFalse(hero_stats.flag_preflop_open_opportunity)
        self.assertFalse(hero_stats.flag_preflop_open)
        self.assertFalse(hero_stats.flag_preflop_first_raise)
        self.assertTrue(hero_stats.flag_preflop_fold)
        self.assertFalse(hero_stats.flag_preflop_limp)
        self.assertFalse(hero_stats.flag_preflop_cold_called)
        self.assertTrue(hero_stats.flag_preflop_face_raise)
        self.assertFalse(hero_stats.flag_preflop_bet)
        self.assertTrue(hero_stats.flag_preflop_3bet_opportunity)
        self.assertFalse(hero_stats.flag_preflop_3bet)
        self.assertFalse(hero_stats.flag_preflop_face_3bet)
        self.assertFalse(hero_stats.flag_preflop_4bet_opportunity)
        self.assertFalse(hero_stats.flag_preflop_4bet)
        self.assertFalse(hero_stats.flag_preflop_face_4bet)
        self.assertFalse(hero_stats.flag_squeeze_opportunity)
        self.assertFalse(hero_stats.flag_squeeze)
        self.assertFalse(hero_stats.flag_face_squeeze)
        self.assertFalse(hero_stats.flag_steal_opportunity)
        self.assertFalse(hero_stats.flag_steal_attempt)
        self.assertFalse(hero_stats.flag_face_steal_attempt)
        self.assertFalse(hero_stats.flag_fold_to_steal_attempt)
        self.assertFalse(hero_stats.flag_blind_defense)
        self.assertFalse(hero_stats.flag_open_shove)
        self.assertFalse(hero_stats.flag_voluntary_all_in_preflop)
        # counts
        self.assertEqual(hero_stats.count_preflop_player_raises, 0)
        self.assertEqual(hero_stats.count_preflop_player_calls, 0)
        self.assertEqual(hero_stats.count_faced_limps, 0)
        # sequences
        # self.assertEqual(hero_stats.preflop_actions_sequence.symbol, "F")
        # amounts
        # self.assertEqual(hero_stats.amount_preflop_effective_stack, 0)




class TestHandHistoryConverter2(unittest.TestCase):
    def setUp(self):
        self.history_path = os.path.join(FILES_DIR, 'example02.json')
        self.converter = HandHistoryConverter()
        self.converter.get_data(self.history_path)

    def test_get_data(self):
        self.assertIsInstance(self.converter.data, dict)

    def test_get_max_players(self):
        self.converter.get_max_players()
        self.assertEqual(self.converter.table.max_players, 3)

    def test_get_buy_in(self):
        buy_in = self.converter.get_buy_in()
        self.assertEqual(BuyIn(prize_pool=4.5, bounty=0, rake=0.5), buy_in)

    def test_get_level(self):
        level = self.converter.get_level()
        self.assertEqual(level.value, 0)
        self.assertEqual(level.bb, 30)
        self.assertEqual(level.sb, 15)
        self.assertEqual(level.ante, 0)

    def test_tournament_name(self):
        tournament_name = self.converter.get_tournament_name()
        self.assertEqual(tournament_name, "Déglingos")

    def test_get_tournament(self):
        self.converter.get_tournament()
        self.assertEqual(self.converter.table.tournament.name, "Déglingos")
        self.assertEqual(self.converter.table.tournament.id, "154140538")
        self.assertEqual(self.converter.table.tournament.level, Level(value=0, bb=30, ante=0))
        self.assertEqual(self.converter.table.tournament.buy_in, BuyIn(prize_pool=4.5, bounty=0, rake=0.5))

    def test_get_button_seat(self):
        self.converter.get_button_seat()
        self.assertEqual(self.converter.table.players.bb_seat, 1)

    def test_get_players(self):
        self.converter.get_players()
        self.assertIsInstance(self.converter.table.players, Players)
        self.assertEqual(self.converter.table.players.len, 3)
        self.assertEqual(self.converter.table.players[1].position, Position.BTN)

    def test_get_player(self):
        player_dict = self.converter.data.get("players").get("1")
        self.converter.get_player(player_dict)
        self.assertEqual(self.converter.table.players[1].name, "jaleo88")
        self.assertEqual(self.converter.table.players[1].stack, 990.0)
        self.assertEqual(self.converter.table.players[1].init_stack, 990.0)
        self.assertEqual(self.converter.table.players[1].bounty, 0.0)

    def test_get_hero(self):
        self.converter.get_players()
        self.converter.get_hero()
        hero = self.converter.table.players["manggy94"]
        self.assertTrue(hero.is_hero)
        self.assertEqual(hero.combo, Combo("6dTh"))

    def test_get_postings(self):
        self.converter.get_tournament()
        self.converter.get_players()
        self.converter.get_postings()
        self.assertEqual(self.converter.table.pot_value, 45)

    def test_get_actions(self):
        self.converter.get_tournament()
        self.converter.get_players()
        self.converter.get_postings()
        self.converter.get_actions()
        self.assertEqual(self.converter.table.pot_value, 165.0)

    def test_convert_history(self):
        table = self.converter.convert_history(self.history_path)
        self.assertEqual(table.pot_value, 0.0)
        self.assertIsInstance(table, Table)


class TestHandHistoryConverter3(unittest.TestCase):
    def setUp(self):
        self.history_path = os.path.join(FILES_DIR, 'example_03.json')
        self.converter = HandHistoryConverter()
        self.converter.get_data(self.history_path)

    def test_get_data(self):
        self.assertIsInstance(self.converter.data, dict)

    def test_get_max_players(self):
        self.converter.get_max_players()
        self.assertEqual(self.converter.table.max_players, 6)

    def test_get_buy_in(self):
        buy_in = self.converter.get_buy_in()
        self.assertEqual(BuyIn(prize_pool=4.5, bounty=0, rake=0.5), buy_in)

    def test_get_level(self):
        level = self.converter.get_level()
        self.assertEqual(level.value, 1)
        self.assertEqual(level.bb, 200)
        self.assertEqual(level.sb, 100)
        self.assertEqual(level.ante, 25)

    def test_tournament_name(self):
        tournament_name = self.converter.get_tournament_name()
        self.assertEqual(tournament_name, "POUR LA DARONNE")

    def test_get_tournament(self):
        self.converter.get_tournament()
        self.assertEqual(self.converter.table.tournament.name, "POUR LA DARONNE")
        self.assertEqual(self.converter.table.tournament.id, "492049891")
        self.assertEqual(self.converter.table.tournament.level, Level(value=1, bb=200, ante=25))
        self.assertEqual(self.converter.table.tournament.buy_in, BuyIn(prize_pool=4.5, bounty=0, rake=0.5))

    def test_get_button_seat(self):
        self.converter.get_button_seat()
        self.assertEqual(self.converter.table.players.bb_seat, 1)

    def test_get_players(self):
        self.converter.get_players()
        self.assertIsInstance(self.converter.table.players, Players)
        self.assertEqual(self.converter.table.players.len, 6)
        self.assertEqual(self.converter.table.players[1].position, Position.CO)

    def test_get_player(self):
        player_dict = self.converter.data.get("players").get("1")
        self.converter.get_player(player_dict)
        self.assertEqual(self.converter.table.players[1].name, "LASYLVE34")
        self.assertEqual(self.converter.table.players[1].stack, 19625.0)
        self.assertEqual(self.converter.table.players[1].init_stack, 19625.0)
        self.assertEqual(self.converter.table.players[1].bounty, 0.0)

    def test_get_hero(self):
        self.converter.get_players()
        self.converter.get_hero()
        hero = self.converter.table.players["manggy94"]
        self.assertTrue(hero.is_hero)
        self.assertEqual(hero.combo, Combo("Qd2c"))

    def test_get_postings(self):
        self.converter.get_tournament()
        self.converter.get_players()
        self.converter.get_postings()
        self.assertEqual(self.converter.table.pot_value, 450)

    def test_get_actions(self):
        self.converter.get_tournament()
        self.converter.get_players()
        self.converter.get_postings()
        self.converter.get_actions()
        self.assertEqual(self.converter.table.pot_value, 1750.0)

    def test_board(self):
        self.converter.get_tournament()
        self.converter.get_players()
        self.converter.get_postings()
        self.converter.get_actions()
        self.assertEqual(self.converter.table.board, Board.from_cards(["Jh", "5h", "2d", "Tc", "8c"]))

    def test_convert_history(self):
        table = self.converter.convert_history(self.history_path)
        self.assertEqual(table.pot_value, 0.0)
        self.assertIsInstance(table, Table)


class TestHandHistoryConverter4(unittest.TestCase):
    def setUp(self):
        self.history_path = os.path.join(FILES_DIR, 'example04.json')
        self.converter = HandHistoryConverter()
        self.converter.get_data(self.history_path)

    def test_convert_history(self):
        table = self.converter.convert_history(self.history_path)
        self.assertEqual(table.pot_value, 0.0)
        self.assertIsInstance(table, Table)


class TestHandHistoryConverter5(unittest.TestCase):
    def setUp(self):
        self.history_path = os.path.join(FILES_DIR, 'example05.json')
        self.converter = HandHistoryConverter()
        self.converter.get_data(self.history_path)

    def test_convert_history(self):
        table = self.converter.convert_history(self.history_path)
        self.assertEqual(table.pot_value, 0.0)
        self.assertIsInstance(table, Table)


class TestHandHistoryConverter6(unittest.TestCase):
    def setUp(self):
        self.history_path = os.path.join(FILES_DIR, 'example06.json')
        self.converter = HandHistoryConverter()
        self.converter.get_data(self.history_path)

    def test_convert_history(self):
        with self.assertRaises(HandConversionError):
            self.converter.convert_history(self.history_path)


class TestHandHistoryConverter7(unittest.TestCase):
    def setUp(self):
        self.history_path = os.path.join(FILES_DIR, 'example07.json')
        self.converter = HandHistoryConverter()
        self.converter.get_data(self.history_path)

    def test_convert_history(self):
        with self.assertRaises(HandConversionError):
            self.converter.convert_history(self.history_path)
