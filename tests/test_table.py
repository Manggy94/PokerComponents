import unittest
import numpy as np
from pkrcomponents.table import Table, Deck, Board, Players, Pot, Tournament, Level, Street
from pkrcomponents.table_player import TablePlayer


class TableTest(unittest.TestCase):

    def setUp(self) -> None:
        self.level = Level(4, 400)
        self.level2 = Level(5, 600)
        self.tournament = Tournament(level=self.level)
        self.p1 = TablePlayer(name="Toto", seat=1, stack=2000)
        self.p2 = TablePlayer(name="Tata", seat=2, stack=2500)
        self.p3 = TablePlayer(name="Titi", seat=6, stack=25000)
        self.p4 = TablePlayer(name="Tété", seat=4, stack=120327)
        self.p5 = TablePlayer(name="Tutu", seat=5, stack=267)
        self.p6 = TablePlayer(name="Tonton", seat=3, stack=11500)
        self.pl_list = [self.p1, self.p2, self.p3, self.p4]
        self.pl_list2 = [self.p1, self.p2, self.p3, self.p4, self.p5, self.p6]

    def test_new_table(self):
        table = Table()
        self.assertIsInstance(table, Table)
        self.assertIsInstance(table.deck, Deck)
        self.assertIsInstance(table.board, Board)
        self.assertIsInstance(table.players, Players)
        self.assertIsInstance(table.pot, Pot)
        self.assertIsInstance(table.street, Street)
        self.assertEqual(table.street, Street.PREFLOP)
        self.assertEqual(table.pot.value, 0)
        self.assertEqual(table.deck.len, 52)
        self.assertEqual(table.board.len, 0)
        with self.assertRaises(ValueError):
            table.max_players = 11
        table.max_players = 9
        self.assertEqual(table.max_players, 9)
        table.level = self.level2
        self.assertEqual(table.level.sb, 300)
        table.add_tournament(self.tournament)
        self.assertEqual(table.level.sb, 200)
        self.assertIsInstance(table.tournament, Tournament)
        self.assertIsInstance(table._tournament, Tournament)
        self.assertEqual(self.level.bb, 400)

    def test_playing_order(self):
        table = Table()
        for pl in self.pl_list:
            pl.sit(table)
        table.level = self.level
        self.p1.distribute("AcKc")
        self.assertEqual(table.playing_order, [2, 4, 6, 1])
        self.assertIsInstance(table.players_waiting, list)
        self.assertEqual(table.players_waiting, [self.p2, self.p4, self.p3, self.p1])
        table._street = Street.FLOP
        self.assertEqual(table.playing_order, [6, 1, 2, 4])
        self.assertEqual(table.players_waiting, [self.p3, self.p1, self.p2, self.p4])
        self.assertEqual(self.p1.stack, 2000)
        self.p2.do_bet(4000)
        self.assertEqual(self.p2.stack, 0)
        self.assertTrue(self.p2.is_all_in)
        self.assertFalse(self.p2.can_play)
        self.assertEqual(table.players_waiting, [self.p3, self.p1, self.p4])
        self.assertEqual(self.p1.to_call, 2000)
        self.assertEqual(self.p1.pot_odds, 1.25)
        self.assertEqual(self.p1.to_call_bb, 5)
        self.p1.do_call()
        self.assertEqual(table.players_waiting, [self.p3, self.p4])
        table.draw_flop("As", "Ad", "Ah")
        self.assertEqual(self.p1.hand_score, 11)
        self.assertEqual(self.p1.rank_class, 2)
        self.assertEqual(self.p1.class_str, "Four of a Kind")

    def test_draws(self):
        table = Table()
        table.draw_flop("As", "Ad", "Ah")
        self.assertEqual(table.board.len, 3)
        self.assertTrue((table.board.values[:3] == np.array(["As", "Ad", "Ah"])).all())
        self.assertRaises(ValueError, lambda: table.draw_flop())
        self.assertRaises(ValueError, lambda: table.draw_turn("As"))
        self.assertRaises(ValueError, lambda: table.draw_river("Jd"))
        table.draw_turn("Ac")
        self.assertEqual(table.board.len, 4)
        self.assertEqual(table.board["turn"], "Ac")
        self.assertTrue((table.board.values[:4] == np.array(["As", "Ad", "Ah", "Ac"])).all())
        self.assertRaises(ValueError, lambda: table.draw_flop())
        self.assertRaises(ValueError, lambda: table.draw_turn("Jd"))
        table.draw_river("Jd")
        self.assertEqual(table.board.len, 5)
        self.assertEqual(table.board["river"], "Jd")
        self.assertTrue((table.board.values == np.array(["As", "Ad", "Ah", "Ac", "Jd"])).all())

    def test_pregame_betting_and_odds(self):
        table = Table()
        table.max_players = 6
        table.add_tournament(self.tournament)
        for pl in self.pl_list:
            pl.sit(table)
        table.bb = 2
        table.players.distribute_positions()
        table.post_pregame()
        self.assertEqual(table.pot.value, 800)
        self.assertEqual(table.pot.highest_bet, table.level.bb)
        self.assertEqual(table.players[1].to_call, 0)
        self.assertEqual(table.players[1].pot_odds, float("inf"))
        self.assertEqual(table.players[1].req_equity, 0)
        self.assertEqual(table.players[1].current_bet, 400)
        self.assertEqual(table.players[2].to_call, 400)
        self.assertEqual(table.players[2].pot_odds, 2)
        self.assertEqual(table.players[2].current_bet, 0)
        self.assertEqual(table.players[2].req_equity, 1/3)
        self.assertEqual(table.players[4].to_call, 400)
        self.assertEqual(table.players[6].to_call, 200)
        self.assertEqual(table.players[6].pot_odds, 4)
        self.assertEqual(table.players[6].req_equity, 1/5)
        self.assertEqual(table.players[6].current_bet, 200)

    def test_game(self):
        table = Table()
        table.max_players = 6
        table.add_tournament(self.tournament)
        self.assertEqual(table.min_bet, 800)
        for pl in self.pl_list2:
            pl.sit(table)
        table.players[1].distribute("TdTh")
        table.players[2].distribute("KdJd")
        table.players[3].distribute("7h7c")
        table.players[4].distribute("8d9d")
        table.players[5].distribute("AsKs")
        table.players.bb = 2
        table.players.distribute_positions()
        self.assertEqual(table.pot.value, 0)
        table.post_pregame()
        self.assertEqual(table.min_bet, 2 * table.level.bb)
        self.assertEqual(table.current_player, self.p6)
        self.assertEqual(table.pot.value, 900)
        self.assertEqual(table.nb_waiting, 6)
        self.assertEqual(table.seat_playing, 3)
        self.assertEqual(table.nb_in_game, 6)
        table.advance_seat_playing()
        self.assertEqual(table.nb_waiting, 6)
        self.assertEqual(table.seat_playing, 3)
        self.assertEqual(table.seats_playing, [3, 4, 5, 6, 1, 2])
        self.assertEqual(table.players_in_game, table.players_waiting)
        self.assertEqual(table.current_player.preflop_bet_amounts, [800, 880, 1000, 1200, 1600, 2800, 4000, 11450.0])
        table.current_player.do_fold()
        self.assertEqual(table.nb_waiting, 5)
        self.assertEqual(table.seat_playing, 3)
        self.assertEqual(table.seats_playing, [4, 5, 6, 1, 2])
        table.advance_seat_playing()
        self.assertEqual(table.seat_playing, 4)
        self.assertEqual(table.seats_playing, [4, 5, 6, 1, 2])
        table.current_player.do_call()
        self.assertEqual(table.nb_waiting, 4)
        self.assertEqual(table.seats_playing, [5, 6, 1, 2])
        self.assertFalse(table.current_player.is_all_in)
        self.assertFalse(table.players[4].can_play)
        table.advance_seat_playing()
        self.assertEqual(table.seat_playing, 5)
        table.current_player.do_call()
        self.assertEqual(table.nb_waiting, 3)
        self.assertEqual(table.seats_playing, [6, 1, 2])
        self.assertTrue(table.current_player.is_all_in)
        self.assertFalse(table.players[5].is_current_player)
        self.assertEqual(table.seat_playing, 6)
        table.current_player.do_bet(3000)
        self.assertEqual(table.min_bet, 800)
        self.assertTrue(table.players[4].can_play)
        self.assertEqual(table.nb_waiting, 3)
        self.assertEqual(table.seats_playing, [4, 1, 2])
        self.assertFalse(table.current_player.can_play)
        table.advance_seat_playing()
        table.min_bet = 5200
        self.assertEqual(table.seat_playing, 1)
        self.assertEqual(table.nb_waiting, 3)
        self.assertTrue(table.players[1].can_play)
        self.assertFalse(table.players[1].is_all_in)
        table.current_player.do_call()
        self.assertTrue(table.players[1].is_all_in)
        self.assertEqual(table.nb_waiting, 2)
        self.assertEqual(table.seats_playing, [4, 2])
        table.advance_seat_playing()
        self.assertFalse(table.players[1].is_current_player)
        self.assertTrue(table.players[2].is_current_player)
        self.assertEqual(table.seat_playing, 2)
        table.current_player.fold()
        self.assertEqual(table.nb_waiting, 1)
        self.assertEqual(table.seats_playing, [4])
        self.assertEqual(table.seat_playing, 4)
        self.assertEqual(table.players_in_game, [table.players[4], table.players[6]])
        table.current_player.do_call()
        self.assertEqual(table.nb_waiting, 0)
        self.assertEqual(table.seats_playing, [])
        self.assertEqual(table.pot.value, 8867)
        self.assertEqual(table.players_involved, [table.players[4], table.players[5], table.players[6], table.players[1]])
        self.assertEqual(table.nb_involved, 4)
        table.flop("Qs", "Js", "Tc")
        self.assertEqual(table.pot.highest_bet, 0)
        for pl in table.players_in_game:
            self.assertEqual(pl.current_bet, 0)
        self.assertEqual(table.playing_order, [1, 2, 3, 4, 5, 6])
        self.assertEqual(table.players_in_game, [table.players[4], table.players[6]])
        self.assertEqual(table.seats_playing, [4, 6])
        self.assertEqual(table.nb_waiting, 2)
        self.assertEqual(
            table.current_player.postflop_bets, [
                {'text': 'Min Bet', 'value': 400.0},
                {'text': '1/4 Pot', 'value': 2217},
                {'text': '1/3 Pot', 'value': 2956},
                {'text': '1/2 Pot', 'value': 4434},
                {'text': '2/3 Pot', 'value': 5911},
                {'text': '3/4 Pot', 'value': 6650},
                {'text': 'Pot', 'value': 8867},
                {'text': 'All-in', 'value': 117277.0}])
        table.current_player.check()
        self.assertEqual(table.seats_playing, [6])
        self.assertEqual(table.nb_waiting, 1)
        table.current_player.bet(11050)
        self.assertEqual(table.seats_playing, [4])
        self.assertEqual(table.nb_waiting, 1)
        self.assertEqual(table.current_player.to_call, 11050)
        self.assertRaises(ValueError, lambda: table.current_player.do_check())
        self.assertRaises(ValueError, lambda: table.current_player.check())
        self.assertEqual(table.pot.value, 19917)
        table.current_player.call()
        self.assertEqual(table.current_player.to_call, 0)
        self.assertEqual(table.pot.value, 30967)
        self.assertTrue(table.next_street_ready)
        self.assertFalse(table.next_hand_ready)
        table.turn("Ts")
        self.assertEqual(table.pot.value, sum([pl.invested for pl in table.players]))
        self.assertEqual(table.players[1].invested, 2000)
        self.assertEqual(table.players[1].max_reward, 6767)
        self.assertEqual(table.players[2].invested, 450)
        self.assertEqual(table.players[2].max_reward, 0)
        self.assertEqual(table.players[3].invested, 50)
        self.assertEqual(table.players[3].max_reward, 0)
        self.assertEqual(table.players[4].invested, 14100)
        self.assertEqual(table.players[4].max_reward, 30967)
        self.assertEqual(table.players[5].invested, 267)
        self.assertEqual(table.players[5].max_reward, 1385)
        self.assertEqual(table.players[6].invested, 14100)
        self.assertEqual(table.players[6].max_reward, 30967)
        table.current_player.bet(table.pot.value)
        self.assertEqual(table.pot.value, 61934)
        self.assertEqual(table.current_player, table.players[6])
        self.assertEqual(table.players_waiting, [table.players[6]])
        table.current_player.bet(1e6)
        table.current_player.bet(1e7)
        self.assertEqual(table.nb_waiting, 0)
        self.assertEqual(table.players_involved, [table.players[1], table.players[4], table.players[5], table.players[6]])
        self.assertEqual(table.players[1].hand_score, 61)
        self.assertEqual(table.players[4].hand_score, 1602)
        self.assertEqual(table.players[5].hand_score, 1)
        table.river("Ah")
        self.assertEqual(table.players[1].hand_score, 59)
        self.assertEqual(table.players[4].hand_score, 1602)
        self.assertEqual(table.players[5].hand_score, 1)
        self.assertEqual(table.unrevealed_players, [table.players[6]])
        self.assertFalse(table.can_parse_winners)
        table.advance_to_showdown()
        self.assertFalse(table.can_parse_winners)
        table.players[6].shows("9h8h")
        self.assertTrue(table.can_parse_winners)
        table.distribute_rewards()
        self.assertEqual(table.players[1].stack, 5382)
        self.assertEqual(table.players[4].stack, 108293.5)
        self.assertEqual(table.players[5].stack, 1385)
        self.assertEqual(table.players[6].stack, 33033.5)
        table.hand_reset()
        self.assertFalse(table.hand_has_started)
        self.assertEqual(table.pot.value, 0)
        self.assertEqual(table.players[1].stack, 5382)
        self.assertIsNone(table.players[1].combo)
        self.assertFalse(table.players[1].folded)
        self.assertFalse(table.players[1].played)

    def test_game2(self):
        table = Table()
        table.max_players = 6
        table.add_tournament(self.tournament)
        self.assertEqual(table.min_bet, 800)
        for pl in self.pl_list2:
            pl.sit(table)
        table.players[1].distribute("TdTh")
        table.players[2].distribute("KdJd")
        table.players[3].distribute("7h7c")
        table.players[4].distribute("8d9d")
        table.players[5].distribute("AsKs")

        table.players[6].shows("9h8h")
        table.players.bb = 2
        table.players.distribute_positions()
        self.assertEqual(table.pot.value, 0)
        table.post_pregame()
        self.assertEqual(table.min_bet_bb, 2)
        self.assertEqual(table.unrevealed_players, [])
        self.assertEqual(table.current_player, self.p6)
        self.assertEqual(table.pot_value_bb, 2.25)
        self.assertEqual(table.average_stack_bb, 67.33)
        table.players[5].bet(400)
        self.assertEqual(table.pot.value, 900+217)

    def test_is_full_or_empty(self):
        table = Table()
        table2 = Table()
        self.assertTrue(table.is_empty)
        self.assertFalse(table.is_full)
        for pl in self.pl_list:
            pl.sit(table)
        self.assertFalse(table.is_full)
        for pl in self.pl_list2:
            pl.sit(table2)
        self.assertTrue(table2.is_full)
        
    def test_set_bb_seat(self):
        table = Table()
        for pl in self.pl_list:
            pl.sit(table)
        table.set_bb_seat(2)
        self.assertEqual(table.players.bb, 2)

    def test_advance_bb_seat(self):
        table = Table()
        for pl in self.pl_list:
            pl.sit(table)
        table.set_bb_seat(2)
        table.advance_bb_seat()
        self.assertEqual(table.players.bb, 4)
        table.advance_bb_seat()
        self.assertEqual(table.players.bb, 6)
        table.advance_bb_seat()
        self.assertEqual(table.players.bb, 1)
        table.advance_bb_seat()
        self.assertEqual(table.players.bb, 2)

    def test_add_remove_player(self):
        table = Table()
        for pl in self.pl_list:
            pl.sit(table)
        self.assertEqual(table.players.occupied_seats, [1, 2, 4, 6])
        table.players.bb = 2
        self.assertEqual(table.players.preflop_ordered_seats, [4, 6, 1, 2])
        table.add_player(self.p5)
        self.assertEqual(table.players.occupied_seats, [1, 2, 4, 5, 6])
        self.assertEqual(table.players.preflop_ordered_seats, [4, 5, 6, 1, 2])
        table.remove_player(self.p5)
        self.assertEqual(table.players.occupied_seats, [1, 2, 4, 6])
        self.assertEqual(table.players.preflop_ordered_seats, [4, 6, 1, 2])

    def test_set_hero(self):
        table = Table()
        for pl in self.pl_list:
            pl.sit(table)
        table.set_hero(self.p1)
        self.assertTrue(self.p1.is_hero)
        self.assertFalse(self.p2.is_hero)
        self.assertFalse(self.p3.is_hero)
        self.assertFalse(self.p4.is_hero)

    def test_bet_factors(self):
        table = Table()
        self.assertEqual(table.preflop_bet_factors, [1, 1.1, 1.25, 1.5, 2, 3.5, 5])
        self.assertEqual(
            table.postflop_bet_factors, [
                {'text': '1/4 Pot', 'value': 0.25},
                {'text': '1/3 Pot', 'value': 0.3333333333333333},
                {'text': '1/2 Pot', 'value': 0.5},
                {'text': '2/3 Pot', 'value': 0.6666666666666666},
                {'text': '3/4 Pot', 'value': 0.75},
                {'text': 'Pot', 'value': 1}
            ]
        )

    def test_start_hand(self):
        table = Table()
        table.add_tournament(self.tournament)
        for pl in self.pl_list:
            table.add_player(pl)
        
        self.assertFalse(table.hand_has_started)
        table.start_hand()
        self.assertTrue(table.hand_has_started)
        self.assertEqual(table.street, Street.PREFLOP)
        self.assertEqual(table.pot.value, 800)
        self.assertEqual(table.players.bb, 1)


if __name__ == '__main__':
    unittest.main()
