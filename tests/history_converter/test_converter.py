import unittest
import os
from datetime import datetime

from pkrcomponents.components.actions.action_move import ActionMove
from pkrcomponents.components.actions.street import Street
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
        self.assertFalse(hero_stats.preflop.flag_vpip)
        self.assertFalse(hero_stats.preflop.flag_open_opportunity)
        self.assertFalse(hero_stats.preflop.flag_open)
        self.assertFalse(hero_stats.preflop.flag_first_raise)
        self.assertTrue(hero_stats.preflop.flag_fold)
        self.assertFalse(hero_stats.preflop.flag_limp)
        self.assertFalse(hero_stats.preflop.flag_cold_called)
        self.assertTrue(hero_stats.preflop.flag_raise_opportunity)
        self.assertFalse(hero_stats.preflop.flag_raise)
        self.assertTrue(hero_stats.preflop.flag_face_raise)
        self.assertTrue(hero_stats.preflop.flag_3bet_opportunity)
        self.assertFalse(hero_stats.preflop.flag_3bet)
        self.assertFalse(hero_stats.preflop.flag_face_3bet)
        self.assertFalse(hero_stats.preflop.flag_4bet_opportunity)
        self.assertFalse(hero_stats.preflop.flag_4bet)
        self.assertFalse(hero_stats.preflop.flag_face_4bet)
        self.assertFalse(hero_stats.preflop.flag_squeeze_opportunity)
        self.assertFalse(hero_stats.preflop.flag_squeeze)
        self.assertFalse(hero_stats.preflop.flag_face_squeeze)
        self.assertFalse(hero_stats.preflop.flag_steal_opportunity)
        self.assertFalse(hero_stats.preflop.flag_steal_attempt)
        self.assertFalse(hero_stats.preflop.flag_face_steal_attempt)
        self.assertFalse(hero_stats.preflop.flag_fold_to_steal_attempt)
        self.assertTrue(hero_stats.preflop.flag_blind_defense_opportunity)
        self.assertFalse(hero_stats.preflop.flag_blind_defense)
        self.assertFalse(hero_stats.preflop.flag_open_shove)
        self.assertFalse(hero_stats.preflop.flag_voluntary_all_in)
        # counts
        self.assertEqual(hero_stats.preflop.count_player_raises, 0)
        self.assertEqual(hero_stats.preflop.count_player_calls, 0)
        self.assertEqual(hero_stats.preflop.count_faced_limps, 0)
        # sequences
        self.assertEqual(hero_stats.preflop.actions_sequence.symbol, "F")
        # amounts
        self.assertEqual(hero_stats.preflop.amount_effective_stack, 18950)
        self.assertEqual(hero_stats.preflop.amount_to_call_facing_bet, 0)
        self.assertEqual(hero_stats.preflop.amount_to_call_facing_2bet, 700)
        self.assertEqual(hero_stats.preflop.amount_to_call_facing_3bet, 0)
        self.assertEqual(hero_stats.preflop.amount_to_call_facing_4bet, 0)
        self.assertEqual(hero_stats.preflop.amount_first_raise_made, 0)
        self.assertEqual(hero_stats.preflop.amount_second_raise_made, 0)
        self.assertEqual(hero_stats.preflop.ratio_to_call_facing_bet, 0)
        self.assertAlmostEqual(hero_stats.preflop.ratio_to_call_facing_2bet, 0.424, 3)
        self.assertEqual(hero_stats.preflop.ratio_to_call_facing_3bet, 0)
        self.assertEqual(hero_stats.preflop.ratio_to_call_facing_4bet, 0)
        self.assertEqual(hero_stats.preflop.ratio_first_raise_made, 0)
        self.assertEqual(hero_stats.preflop.ratio_second_raise_made, 0)
        self.assertEqual(hero_stats.preflop.total_bet_amount, 0)
        # moves
        self.assertEqual(hero_stats.preflop.move_facing_2bet, ActionMove.FOLD)
        self.assertIsNone(hero_stats.preflop.move_facing_3bet)
        self.assertIsNone(hero_stats.preflop.move_facing_4bet)
        self.assertIsNone(hero_stats.preflop.move_facing_squeeze)
        self.assertIsNone(hero_stats.preflop.move_facing_steal_attempt)
        villain_player = table.players["GoToVG"]
        villain_stats = villain_player.hand_stats
        self.assertTrue(villain_stats.preflop.flag_vpip)
        self.assertFalse(villain_stats.preflop.flag_open_opportunity)
        self.assertFalse(villain_stats.preflop.flag_open)
        self.assertTrue(villain_stats.preflop.flag_first_raise)
        self.assertFalse(villain_stats.preflop.flag_fold)
        self.assertFalse(villain_stats.preflop.flag_limp)
        self.assertFalse(villain_stats.preflop.flag_cold_called)
        self.assertTrue(villain_stats.preflop.flag_raise_opportunity)
        self.assertTrue(villain_stats.preflop.flag_raise)
        self.assertFalse(villain_stats.preflop.flag_face_raise)
        self.assertFalse(villain_stats.preflop.flag_3bet_opportunity)
        self.assertFalse(villain_stats.preflop.flag_3bet)
        self.assertFalse(villain_stats.preflop.flag_face_3bet)
        self.assertFalse(villain_stats.preflop.flag_4bet_opportunity)
        self.assertFalse(villain_stats.preflop.flag_4bet)
        self.assertFalse(villain_stats.preflop.flag_face_4bet)
        self.assertFalse(villain_stats.preflop.flag_squeeze_opportunity)
        self.assertFalse(villain_stats.preflop.flag_squeeze)
        self.assertFalse(villain_stats.preflop.flag_face_squeeze)
        self.assertFalse(villain_stats.preflop.flag_steal_opportunity)
        self.assertFalse(villain_stats.preflop.flag_steal_attempt)
        self.assertFalse(villain_stats.preflop.flag_face_steal_attempt)
        self.assertFalse(villain_stats.preflop.flag_fold_to_steal_attempt)
        self.assertFalse(villain_stats.preflop.flag_blind_defense_opportunity)
        self.assertFalse(villain_stats.preflop.flag_blind_defense)
        self.assertFalse(villain_stats.preflop.flag_open_shove)
        self.assertFalse(villain_stats.preflop.flag_voluntary_all_in)
        # counts
        self.assertEqual(villain_stats.preflop.count_player_raises, 1)
        self.assertEqual(villain_stats.preflop.count_player_calls, 0)
        self.assertEqual(villain_stats.preflop.count_faced_limps, 0)
        # sequences
        self.assertEqual(villain_stats.preflop.actions_sequence.symbol, "R")
        # amounts
        self.assertEqual(villain_stats.preflop.amount_effective_stack, 21605)
        self.assertEqual(villain_stats.preflop.amount_to_call_facing_bet, 100)
        self.assertEqual(villain_stats.preflop.amount_to_call_facing_2bet, 0)
        self.assertEqual(villain_stats.preflop.amount_to_call_facing_3bet, 0)
        self.assertEqual(villain_stats.preflop.amount_to_call_facing_4bet, 0)
        self.assertEqual(villain_stats.preflop.amount_first_raise_made, 800)
        self.assertEqual(villain_stats.preflop.amount_second_raise_made, 0)
        self.assertAlmostEqual(villain_stats.preflop.ratio_to_call_facing_bet, 0.06, 2)
        self.assertEqual(villain_stats.preflop.ratio_to_call_facing_2bet, 0)
        self.assertEqual(villain_stats.preflop.ratio_to_call_facing_3bet, 0)
        self.assertEqual(villain_stats.preflop.ratio_to_call_facing_4bet, 0)
        self.assertAlmostEqual(villain_stats.preflop.ratio_first_raise_made, 0.48, 2)
        self.assertEqual(villain_stats.preflop.ratio_second_raise_made, 0)
        self.assertEqual(villain_stats.preflop.total_bet_amount, 800)
        # moves
        self.assertIsNone(villain_stats.preflop.move_facing_2bet)
        self.assertIsNone(villain_stats.preflop.move_facing_3bet)
        self.assertIsNone(villain_stats.preflop.move_facing_4bet)
        self.assertIsNone(villain_stats.preflop.move_facing_squeeze)
        self.assertIsNone(villain_stats.preflop.move_facing_steal_attempt)
        # Flop
        # Flags
        self.assertFalse(hero_stats.flop.flag_saw)
        self.assertTrue(villain_stats.flop.flag_saw)
        self.assertFalse(hero_stats.flop.flag_first_to_talk)
        self.assertTrue(villain_stats.flop.flag_first_to_talk)
        self.assertFalse(hero_stats.flop.flag_has_position)
        self.assertFalse(villain_stats.flop.flag_has_position)
        self.assertFalse(hero_stats.flop.flag_bet)
        self.assertFalse(villain_stats.flop.flag_bet)
        self.assertFalse(hero_stats.flop.flag_open_opportunity)
        self.assertTrue(villain_stats.flop.flag_open_opportunity)
        self.assertFalse(hero_stats.flop.flag_open)
        self.assertFalse(villain_stats.flop.flag_open)
        self.assertFalse(hero_stats.flop.flag_cbet_opportunity)
        self.assertTrue(villain_stats.flop.flag_cbet_opportunity)
        self.assertFalse(hero_stats.flop.flag_cbet)
        self.assertFalse(villain_stats.flop.flag_cbet)
        self.assertFalse(hero_stats.flop.flag_face_cbet)
        self.assertFalse(villain_stats.flop.flag_face_cbet)
        self.assertFalse(hero_stats.flop.flag_donk_bet_opportunity)
        self.assertFalse(villain_stats.flop.flag_donk_bet_opportunity)
        self.assertFalse(hero_stats.flop.flag_donk_bet)
        self.assertFalse(villain_stats.flop.flag_donk_bet)
        self.assertFalse(hero_stats.flop.flag_face_donk_bet)
        self.assertFalse(villain_stats.flop.flag_face_donk_bet)
        self.assertFalse(hero_stats.flop.flag_first_raise)
        self.assertFalse(villain_stats.flop.flag_first_raise)
        self.assertFalse(hero_stats.flop.flag_fold)
        self.assertFalse(villain_stats.flop.flag_fold)
        self.assertFalse(hero_stats.flop.flag_check)
        self.assertTrue(villain_stats.flop.flag_check)
        self.assertFalse(hero_stats.flop.flag_check_raise)
        self.assertFalse(villain_stats.flop.flag_check_raise)
        self.assertFalse(hero_stats.flop.flag_3bet_opportunity)
        self.assertFalse(villain_stats.flop.flag_3bet_opportunity)
        self.assertFalse(hero_stats.flop.flag_3bet)
        self.assertFalse(villain_stats.flop.flag_3bet)
        self.assertFalse(hero_stats.flop.flag_face_3bet)
        self.assertFalse(villain_stats.flop.flag_face_3bet)
        self.assertFalse(hero_stats.flop.flag_4bet_opportunity)
        self.assertFalse(villain_stats.flop.flag_4bet_opportunity)
        self.assertFalse(hero_stats.flop.flag_4bet)
        self.assertFalse(villain_stats.flop.flag_4bet)
        self.assertFalse(hero_stats.flop.flag_face_4bet)
        self.assertFalse(villain_stats.flop.flag_face_4bet)
        # counts
        self.assertEqual(hero_stats.flop.count_player_raises, 0)
        self.assertEqual(hero_stats.flop.count_player_calls, 0)
        self.assertEqual(villain_stats.flop.count_player_raises, 0)
        self.assertEqual(villain_stats.flop.count_player_calls, 0)
        # sequences
        self.assertEqual(hero_stats.flop.actions_sequence.symbol, "")
        self.assertEqual(villain_stats.flop.actions_sequence.symbol, "X")
        # amounts
        self.assertEqual(hero_stats.flop.amount_effective_stack, 0)
        self.assertEqual(villain_stats.flop.amount_effective_stack, 20905)
        self.assertEqual(hero_stats.flop.amount_to_call_facing_bet, 0)
        self.assertEqual(villain_stats.flop.amount_to_call_facing_bet, 0)
        self.assertEqual(hero_stats.flop.amount_to_call_facing_2bet, 0)
        self.assertEqual(villain_stats.flop.amount_to_call_facing_2bet, 0)
        self.assertEqual(hero_stats.flop.amount_to_call_facing_3bet, 0)
        self.assertEqual(villain_stats.flop.amount_to_call_facing_3bet, 0)
        self.assertEqual(hero_stats.flop.amount_to_call_facing_4bet, 0)
        self.assertEqual(villain_stats.flop.amount_to_call_facing_4bet, 0)
        self.assertEqual(hero_stats.flop.amount_bet_made, 0)
        self.assertEqual(villain_stats.flop.amount_bet_made, 0)
        self.assertEqual(hero_stats.flop.amount_first_raise_made, 0)
        self.assertEqual(villain_stats.flop.amount_first_raise_made, 0)
        self.assertEqual(hero_stats.flop.amount_second_raise_made, 0)
        self.assertEqual(villain_stats.flop.amount_second_raise_made, 0)
        self.assertEqual(hero_stats.flop.ratio_to_call_facing_bet, 0)
        self.assertEqual(villain_stats.flop.ratio_to_call_facing_bet, 0)
        self.assertEqual(hero_stats.flop.ratio_to_call_facing_2bet, 0)
        self.assertEqual(villain_stats.flop.ratio_to_call_facing_2bet, 0)
        self.assertEqual(hero_stats.flop.ratio_to_call_facing_3bet, 0)
        self.assertEqual(villain_stats.flop.ratio_to_call_facing_3bet, 0)
        self.assertEqual(hero_stats.flop.ratio_to_call_facing_4bet, 0)
        self.assertEqual(villain_stats.flop.ratio_to_call_facing_4bet, 0)
        self.assertEqual(hero_stats.flop.ratio_bet_made, 0)
        self.assertEqual(villain_stats.flop.ratio_bet_made, 0)
        self.assertEqual(hero_stats.flop.ratio_first_raise_made, 0)
        self.assertEqual(villain_stats.flop.ratio_first_raise_made, 0)
        self.assertEqual(hero_stats.flop.ratio_second_raise_made, 0)
        self.assertEqual(villain_stats.flop.ratio_second_raise_made, 0)
        self.assertEqual(hero_stats.flop.total_bet_amount, 0)
        self.assertEqual(villain_stats.flop.total_bet_amount, 0)
        # moves
        self.assertIsNone(hero_stats.flop.move_facing_bet)
        self.assertIsNone(villain_stats.flop.move_facing_bet)
        self.assertIsNone(hero_stats.flop.move_facing_2bet)
        self.assertIsNone(villain_stats.flop.move_facing_2bet)
        self.assertIsNone(hero_stats.flop.move_facing_3bet)
        self.assertIsNone(villain_stats.flop.move_facing_3bet)
        self.assertIsNone(hero_stats.flop.move_facing_4bet)
        self.assertIsNone(villain_stats.flop.move_facing_4bet)
        self.assertIsNone(hero_stats.flop.move_facing_cbet)
        self.assertIsNone(villain_stats.flop.move_facing_cbet)
        self.assertIsNone(hero_stats.flop.move_facing_donk_bet)
        self.assertIsNone(villain_stats.flop.move_facing_donk_bet)
        # Turn
        # Flags
        self.assertFalse(hero_stats.turn.flag_saw)
        self.assertTrue(villain_stats.turn.flag_saw)
        self.assertFalse(hero_stats.turn.flag_first_to_talk)
        self.assertTrue(villain_stats.turn.flag_first_to_talk)
        self.assertFalse(hero_stats.turn.flag_has_position)
        self.assertFalse(villain_stats.turn.flag_has_position)
        self.assertFalse(hero_stats.turn.flag_bet)
        self.assertTrue(villain_stats.turn.flag_bet)
        self.assertFalse(hero_stats.turn.flag_open_opportunity)
        self.assertTrue(villain_stats.turn.flag_open_opportunity)
        self.assertFalse(hero_stats.turn.flag_open)
        self.assertTrue(villain_stats.turn.flag_open)
        self.assertFalse(hero_stats.turn.flag_cbet_opportunity)
        self.assertFalse(villain_stats.turn.flag_cbet_opportunity)
        self.assertFalse(hero_stats.turn.flag_cbet)
        self.assertFalse(villain_stats.turn.flag_cbet)
        self.assertFalse(hero_stats.turn.flag_face_cbet)
        self.assertFalse(villain_stats.turn.flag_face_cbet)
        self.assertFalse(hero_stats.turn.flag_donk_bet_opportunity)
        self.assertFalse(villain_stats.turn.flag_donk_bet_opportunity)
        self.assertFalse(hero_stats.turn.flag_donk_bet)
        self.assertFalse(villain_stats.turn.flag_donk_bet)
        self.assertFalse(hero_stats.turn.flag_face_donk_bet)
        self.assertFalse(villain_stats.turn.flag_face_donk_bet)
        self.assertFalse(hero_stats.turn.flag_first_raise)
        self.assertFalse(villain_stats.turn.flag_first_raise)
        self.assertFalse(hero_stats.turn.flag_fold)
        self.assertFalse(villain_stats.turn.flag_fold)
        self.assertFalse(hero_stats.turn.flag_check)
        self.assertFalse(villain_stats.turn.flag_check)
        self.assertFalse(hero_stats.turn.flag_check_raise)
        self.assertFalse(villain_stats.turn.flag_check_raise)
        self.assertFalse(hero_stats.turn.flag_face_raise)
        self.assertFalse(villain_stats.turn.flag_face_raise)
        self.assertFalse(hero_stats.turn.flag_3bet_opportunity)
        self.assertFalse(villain_stats.turn.flag_3bet_opportunity)
        self.assertFalse(hero_stats.turn.flag_3bet)
        self.assertFalse(villain_stats.turn.flag_3bet)
        self.assertFalse(hero_stats.turn.flag_face_3bet)
        self.assertFalse(villain_stats.turn.flag_face_3bet)
        self.assertFalse(hero_stats.turn.flag_4bet_opportunity)
        self.assertFalse(villain_stats.turn.flag_4bet_opportunity)
        self.assertFalse(hero_stats.turn.flag_4bet)
        self.assertFalse(villain_stats.turn.flag_4bet)
        self.assertFalse(hero_stats.turn.flag_face_4bet)
        self.assertFalse(villain_stats.turn.flag_face_4bet)
        # counts
        self.assertEqual(hero_stats.turn.count_player_raises, 0)
        self.assertEqual(hero_stats.turn.count_player_calls, 0)
        self.assertEqual(villain_stats.turn.count_player_raises, 0)
        self.assertEqual(villain_stats.turn.count_player_calls, 0)
        # sequences
        self.assertEqual(hero_stats.turn.actions_sequence.symbol, "")
        self.assertEqual(villain_stats.turn.actions_sequence.symbol, "B")
        # amounts
        self.assertEqual(hero_stats.turn.amount_effective_stack, 0)
        self.assertEqual(villain_stats.turn.amount_effective_stack, 20905)
        self.assertEqual(hero_stats.turn.amount_to_call_facing_bet, 0)
        self.assertEqual(villain_stats.turn.amount_to_call_facing_bet, 0)
        self.assertEqual(hero_stats.turn.amount_to_call_facing_2bet, 0)
        self.assertEqual(villain_stats.turn.amount_to_call_facing_2bet, 0)
        self.assertEqual(hero_stats.turn.amount_to_call_facing_3bet, 0)
        self.assertEqual(villain_stats.turn.amount_to_call_facing_3bet, 0)
        self.assertEqual(hero_stats.turn.amount_to_call_facing_4bet, 0)
        self.assertEqual(villain_stats.turn.amount_to_call_facing_4bet, 0)
        self.assertEqual(hero_stats.turn.amount_bet_made, 0)
        self.assertEqual(villain_stats.turn.amount_bet_made, 1000)
        self.assertEqual(hero_stats.turn.amount_first_raise_made, 0)
        self.assertEqual(villain_stats.turn.amount_first_raise_made, 0)
        self.assertEqual(hero_stats.turn.amount_second_raise_made, 0)
        self.assertEqual(villain_stats.turn.amount_second_raise_made, 0)
        self.assertEqual(hero_stats.turn.ratio_to_call_facing_bet, 0)
        self.assertEqual(villain_stats.turn.ratio_to_call_facing_bet, 0)
        self.assertEqual(hero_stats.turn.ratio_to_call_facing_2bet, 0)
        self.assertEqual(villain_stats.turn.ratio_to_call_facing_2bet, 0)
        self.assertEqual(hero_stats.turn.ratio_to_call_facing_3bet, 0)
        self.assertEqual(villain_stats.turn.ratio_to_call_facing_3bet, 0)
        self.assertEqual(hero_stats.turn.ratio_to_call_facing_4bet, 0)
        self.assertEqual(villain_stats.turn.ratio_to_call_facing_4bet, 0)
        self.assertEqual(hero_stats.turn.ratio_bet_made, 0)
        self.assertAlmostEqual(villain_stats.turn.ratio_bet_made, 0.25, 2)
        self.assertEqual(hero_stats.turn.ratio_first_raise_made, 0)
        self.assertEqual(villain_stats.turn.ratio_first_raise_made, 0)
        self.assertEqual(hero_stats.turn.ratio_second_raise_made, 0)
        self.assertEqual(villain_stats.turn.ratio_second_raise_made, 0)
        self.assertEqual(hero_stats.turn.total_bet_amount, 0)
        self.assertEqual(villain_stats.turn.total_bet_amount, 1000)
        # moves
        self.assertIsNone(hero_stats.turn.move_facing_bet)
        self.assertIsNone(villain_stats.turn.move_facing_bet)
        self.assertIsNone(hero_stats.turn.move_facing_2bet)
        self.assertIsNone(villain_stats.turn.move_facing_2bet)
        self.assertIsNone(hero_stats.turn.move_facing_3bet)
        self.assertIsNone(villain_stats.turn.move_facing_3bet)
        self.assertIsNone(hero_stats.turn.move_facing_4bet)
        self.assertIsNone(villain_stats.turn.move_facing_4bet)
        self.assertIsNone(hero_stats.turn.move_facing_cbet)
        self.assertIsNone(villain_stats.turn.move_facing_cbet)
        self.assertIsNone(hero_stats.turn.move_facing_donk_bet)
        self.assertIsNone(villain_stats.turn.move_facing_donk_bet)
        # River
        # Flags
        self.assertFalse(hero_stats.river.flag_saw)
        self.assertTrue(villain_stats.river.flag_saw)
        self.assertFalse(hero_stats.river.flag_first_to_talk)
        self.assertTrue(villain_stats.river.flag_first_to_talk)
        self.assertFalse(hero_stats.river.flag_has_position)
        self.assertFalse(villain_stats.river.flag_has_position)
        self.assertFalse(hero_stats.river.flag_bet)
        self.assertTrue(villain_stats.river.flag_bet)
        self.assertFalse(hero_stats.river.flag_open_opportunity)
        self.assertTrue(villain_stats.river.flag_open_opportunity)
        self.assertFalse(hero_stats.river.flag_open)
        self.assertTrue(villain_stats.river.flag_open)
        self.assertFalse(hero_stats.river.flag_cbet_opportunity)
        self.assertTrue(villain_stats.river.flag_cbet_opportunity)
        self.assertFalse(hero_stats.river.flag_cbet)
        self.assertTrue(villain_stats.river.flag_cbet)
        self.assertFalse(hero_stats.river.flag_face_cbet)
        self.assertFalse(villain_stats.river.flag_face_cbet)
        self.assertFalse(hero_stats.river.flag_donk_bet_opportunity)
        self.assertFalse(villain_stats.river.flag_donk_bet_opportunity)
        self.assertFalse(hero_stats.river.flag_donk_bet)
        self.assertFalse(villain_stats.river.flag_donk_bet)
        self.assertFalse(hero_stats.river.flag_face_donk_bet)
        self.assertFalse(villain_stats.river.flag_face_donk_bet)
        self.assertFalse(hero_stats.river.flag_first_raise)
        self.assertFalse(villain_stats.river.flag_first_raise)
        self.assertFalse(hero_stats.river.flag_fold)
        self.assertFalse(villain_stats.river.flag_fold)
        self.assertFalse(hero_stats.river.flag_check)
        self.assertFalse(villain_stats.river.flag_check)
        self.assertFalse(hero_stats.river.flag_check_raise)
        self.assertFalse(villain_stats.river.flag_check_raise)
        self.assertFalse(hero_stats.river.flag_face_raise)
        self.assertFalse(villain_stats.river.flag_face_raise)
        self.assertFalse(hero_stats.river.flag_3bet_opportunity)
        self.assertFalse(villain_stats.river.flag_3bet_opportunity)
        self.assertFalse(hero_stats.river.flag_3bet)
        self.assertFalse(villain_stats.river.flag_3bet)
        self.assertFalse(hero_stats.river.flag_face_3bet)
        self.assertFalse(villain_stats.river.flag_face_3bet)
        self.assertFalse(hero_stats.river.flag_4bet_opportunity)
        self.assertFalse(villain_stats.river.flag_4bet_opportunity)
        self.assertFalse(hero_stats.river.flag_4bet)
        self.assertFalse(villain_stats.river.flag_4bet)
        self.assertFalse(hero_stats.river.flag_face_4bet)
        self.assertFalse(villain_stats.river.flag_face_4bet)
        # counts
        self.assertEqual(hero_stats.river.count_player_raises, 0)
        self.assertEqual(hero_stats.river.count_player_calls, 0)
        self.assertEqual(villain_stats.river.count_player_raises, 0)
        self.assertEqual(villain_stats.river.count_player_calls, 0)
        # sequences
        self.assertEqual(hero_stats.river.actions_sequence.symbol, "")
        self.assertEqual(villain_stats.river.actions_sequence.symbol, "B")
        # amounts
        self.assertEqual(hero_stats.river.amount_effective_stack, 0)
        self.assertEqual(villain_stats.river.amount_effective_stack, 16623)
        self.assertEqual(hero_stats.river.amount_to_call_facing_bet, 0)
        self.assertEqual(villain_stats.river.amount_to_call_facing_bet, 0)
        self.assertEqual(hero_stats.river.amount_to_call_facing_2bet, 0)
        self.assertEqual(villain_stats.river.amount_to_call_facing_2bet, 0)
        self.assertEqual(hero_stats.river.amount_to_call_facing_3bet, 0)
        self.assertEqual(villain_stats.river.amount_to_call_facing_3bet, 0)
        self.assertEqual(hero_stats.river.amount_to_call_facing_4bet, 0)
        self.assertEqual(villain_stats.river.amount_to_call_facing_4bet, 0)
        self.assertEqual(hero_stats.river.amount_bet_made, 0)
        self.assertEqual(villain_stats.river.amount_bet_made, 2525)
        self.assertEqual(hero_stats.river.amount_first_raise_made, 0)
        self.assertEqual(villain_stats.river.amount_first_raise_made, 0)
        self.assertEqual(hero_stats.river.amount_second_raise_made, 0)
        self.assertEqual(villain_stats.river.amount_second_raise_made, 0)
        self.assertEqual(hero_stats.river.ratio_to_call_facing_bet, 0)
        self.assertEqual(villain_stats.river.ratio_to_call_facing_bet, 0)
        self.assertEqual(hero_stats.river.ratio_to_call_facing_2bet, 0)
        self.assertEqual(villain_stats.river.ratio_to_call_facing_2bet, 0)
        self.assertEqual(hero_stats.river.ratio_to_call_facing_3bet, 0)
        self.assertEqual(villain_stats.river.ratio_to_call_facing_3bet, 0)
        self.assertEqual(hero_stats.river.ratio_to_call_facing_4bet, 0)
        self.assertEqual(villain_stats.river.ratio_to_call_facing_4bet, 0)
        self.assertEqual(hero_stats.river.ratio_bet_made, 0)
        self.assertAlmostEqual(villain_stats.river.ratio_bet_made, 1/3, 2)
        self.assertEqual(hero_stats.river.ratio_first_raise_made, 0)
        self.assertEqual(villain_stats.river.ratio_first_raise_made, 0)
        self.assertEqual(hero_stats.river.ratio_second_raise_made, 0)
        self.assertEqual(villain_stats.river.ratio_second_raise_made, 0)
        self.assertEqual(hero_stats.river.total_bet_amount, 0)
        self.assertEqual(villain_stats.river.total_bet_amount, 2525)
        # moves
        self.assertIsNone(hero_stats.river.move_facing_bet)
        self.assertIsNone(villain_stats.river.move_facing_bet)
        self.assertIsNone(hero_stats.river.move_facing_2bet)
        self.assertIsNone(villain_stats.river.move_facing_2bet)
        self.assertIsNone(hero_stats.river.move_facing_3bet)
        self.assertIsNone(villain_stats.river.move_facing_3bet)
        self.assertIsNone(hero_stats.river.move_facing_4bet)
        self.assertIsNone(villain_stats.river.move_facing_4bet)
        self.assertIsNone(hero_stats.river.move_facing_cbet)
        self.assertIsNone(villain_stats.river.move_facing_cbet)
        self.assertIsNone(hero_stats.river.move_facing_donk_bet)
        self.assertIsNone(villain_stats.river.move_facing_donk_bet)
        # General
        self.assertEqual(hero_stats.general.combo, Combo("5h2c"))
        self.assertIsNone(villain_stats.general.combo)
        self.assertEqual(hero_stats.general.starting_stack, 19175)
        self.assertEqual(villain_stats.general.starting_stack, 26609)
        self.assertEqual(hero_stats.general.total_bet_amount, 0)
        self.assertEqual(villain_stats.general.total_bet_amount, 4325)
        self.assertTrue(hero_stats.general.flag_is_hero)
        self.assertFalse(villain_stats.general.flag_is_hero)
        self.assertIsNone(hero_stats.general.face_covering_bet_street)
        self.assertIsNone(villain_stats.general.face_covering_bet_street)
        self.assertIsNone(hero_stats.general.facing_covering_bet_move)
        self.assertIsNone(villain_stats.general.facing_covering_bet_move)
        self.assertEqual(hero_stats.general.fold_street, Street.PREFLOP)
        self.assertIsNone(villain_stats.general.fold_street)
        self.assertIsNone(hero_stats.general.all_in_street)
        self.assertIsNone(villain_stats.general.all_in_street)
        self.assertIsNone(hero_stats.general.face_all_in_street)
        self.assertIsNone(villain_stats.general.face_all_in_street)
        self.assertIsNone(hero_stats.general.facing_all_in_move)
        self.assertIsNone(villain_stats.general.facing_all_in_move)
        self.assertEqual(hero_stats.general.amount_won, 0)
        self.assertEqual(villain_stats.general.amount_won, 7575)
        self.assertFalse(hero_stats.general.flag_won_hand)
        self.assertTrue(villain_stats.general.flag_won_hand)


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
        self.history_path = os.path.join(FILES_DIR, 'example03.json')
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
        self.converter.convert_history(self.history_path)


class TestHandHistoryConverter8(unittest.TestCase):
    def setUp(self):
        self.history_path = os.path.join(FILES_DIR, 'example08.json')
        self.converter = HandHistoryConverter()
        self.converter.get_data(self.history_path)

    def test_convert_history(self):
        with self.assertRaises(HandConversionError):
            self.converter.convert_history(self.history_path)


class TestHandHistoryConverter9(unittest.TestCase):
    def setUp(self):
        self.history_path = os.path.join(FILES_DIR, 'example09.json')
        self.converter = HandHistoryConverter()
        self.converter.get_data(self.history_path)

    def test_convert_history(self):
        with self.assertRaises(HandConversionError):
            self.converter.convert_history(self.history_path)


class TestHandHistoryConverter10(unittest.TestCase):
    def setUp(self):
        self.history_path = os.path.join(FILES_DIR, 'example10.json')
        self.converter = HandHistoryConverter()
        self.converter.get_data(self.history_path)

    def test_convert_history(self):
        #with self.assertRaises(HandConversionError):
        self.converter.convert_history(self.history_path)
