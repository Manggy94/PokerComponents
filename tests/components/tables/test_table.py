import unittest
import numpy as np
from pkrcomponents.components.actions.action import FoldAction, CheckAction, CallAction, BetAction, RaiseAction
from pkrcomponents.components.cards.card import Card
from pkrcomponents.components.cards.flop import Flop
from pkrcomponents.components.tournaments.buy_in import BuyIn
from pkrcomponents.components.tables.table import Table, Board, Players, Pot, Tournament, Level
from pkrcomponents.components.actions.street import Street
from pkrcomponents.components.cards.deck import Deck
from pkrcomponents.components.players.table_player import TablePlayer
from pkrcomponents.components.utils.exceptions import (NotSufficientRaiseError, ShowdownNotReachedError,
                                                       NotSufficientBetError, CannotParseWinnersError)


class TableTest(unittest.TestCase):

    def setUp(self) -> None:
        self.level = Level(4, 400)
        self.level2 = Level(5, 600)
        self.tournament = Tournament(level=self.level)
        self.p1 = TablePlayer(name="Toto", seat=1, init_stack=2000)
        self.p2 = TablePlayer(name="Tata", seat=2, init_stack=2500)
        self.p3 = TablePlayer(name="Titi", seat=6, init_stack=25000)
        self.p4 = TablePlayer(name="Tété", seat=4, init_stack=120327)
        self.p5 = TablePlayer(name="Tutu", seat=5, init_stack=267)
        self.p6 = TablePlayer(name="Tonton", seat=3, init_stack=11500)
        self.pl_list = [self.p1, self.p2, self.p3, self.p4]
        self.pl_list2 = [self.p1, self.p2, self.p3, self.p4, self.p5, self.p6]

    def test_new_table(self):
        table = Table()
        self.assertIsInstance(table, Table)
        self.assertIsInstance(table.deck, Deck)
        self.assertIsInstance(table.board, Board)
        self.assertIsInstance(table.players, Players)
        self.assertIsInstance(table.pot, Pot)
        self.assertIsNone(table.tournament)
        self.assertIsNone(table.street)
        self.assertEqual(table.postings, [])
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
        self.assertEqual(self.level.bb, 400)
        self.assertFalse(table.hand_has_started)

    def test_playing_order(self):
        table = Table()
        for pl in self.pl_list:
            pl.sit(table)
        table.level = self.level
        self.assertEqual(table.postings, [])
        self.assertEqual(table.pot_value, 0)
        self.assertEqual(table.pot.highest_bet, 0)
        self.assertEqual(table.cnt_bets, 0)
        self.assertEqual(table.cnt_calls, 0)
        table.start_hand()
        self.assertEqual(len(table.postings), 6)
        self.assertEqual(table.pot_value, 800)
        self.assertEqual(table.pot.highest_bet, 400)
        self.assertEqual(table.cnt_bets, 1)
        self.assertEqual(table.cnt_calls, 0)
        self.p1.distribute("AcKc")
        self.assertEqual(table.playing_order, [2, 4, 6, 1])
        self.assertIsInstance(table.players_waiting, list)
        self.assertEqual(table.players_waiting, [self.p2, self.p4, self.p3, self.p1])
        table.street = Street.FLOP
        self.assertEqual(table.playing_order, [6, 1, 2, 4])
        self.assertEqual(table.players_waiting, [self.p3, self.p1, self.p2, self.p4])
        self.assertEqual(self.p1.stack, 1550)
        bet_action = BetAction(self.p2, 4000)
        bet_action.play()
        self.assertEqual(self.p2.stack, 0)
        self.assertTrue(self.p2.is_all_in)
        self.assertFalse(self.p2.can_play)
        self.assertEqual(table.players_waiting, [self.p3, self.p1, self.p4])
        self.assertEqual(self.p1.to_call, 1550)
        self.assertAlmostEqual(self.p1.pot_odds, 2.10, 2)
        self.assertAlmostEqual(self.p1.to_call_bb, 3.875, 3)
        action = CallAction(self.p1)
        action.execute()
        self.assertEqual(table.players_waiting, [self.p3, self.p4])
        table.draw_flop("As", "Ad", "Ah")
        self.assertEqual(self.p1.hand_score, 11)
        self.assertEqual(self.p1.rank_class, 2)
        self.assertEqual(self.p1.class_str, "Four of a Kind")

    def test_draws(self):
        table = Table()
        table.draw_flop("As", "Ad", "Ah")
        self.assertEqual(table.board.len, 3)
        self.assertEqual(table.board.flop, Flop("As", "Ad", "Ah"))
        self.assertRaises(ValueError, lambda: table.draw_flop())
        self.assertRaises(ValueError, lambda: table.draw_turn("As"))
        self.assertRaises(ValueError, lambda: table.draw_river("Jd"))
        table.draw_turn("Ac")
        self.assertEqual(table.board.len, 4)
        self.assertEqual(table.board.turn, Card("Ac"))
        self.assertEqual(table.board.cards.astype(str).values[:4].tolist(),  ["As", "Ah", "Ad", "Ac"])
        self.assertRaises(ValueError, lambda: table.draw_flop())
        self.assertRaises(ValueError, lambda: table.draw_turn("Jd"))
        table.draw_river("Jd")
        self.assertEqual(table.board.len, 5)
        self.assertEqual(table.board.cards["river"], Card("Jd"))
        self.assertTrue((table.board.cards.astype(str).values == np.array(["As", "Ah", "Ad", "Ac", "Jd"])).all())

    def test_pregame_betting_and_odds(self):
        table = Table()
        table.max_players = 6
        table.add_tournament(self.tournament)
        for pl in self.pl_list:
            pl.sit(table)
        table.players.bb_seat = 1
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
        self.assertEqual(table.players.bb_seat, 2)

    def test_advance_bb_seat(self):
        table = Table()
        for pl in self.pl_list:
            pl.sit(table)
        table.set_bb_seat(2)
        table.advance_bb_seat()
        self.assertEqual(table.players.bb_seat, 4)
        table.advance_bb_seat()
        self.assertEqual(table.players.bb_seat, 6)
        table.advance_bb_seat()
        self.assertEqual(table.players.bb_seat, 1)
        table.advance_bb_seat()
        self.assertEqual(table.players.bb_seat, 2)

    def test_add_remove_player(self):
        table = Table()
        for pl in self.pl_list:
            pl.sit(table)
        self.assertEqual(table.players.occupied_seats, [1, 2, 4, 6])
        table.players.bb_seat = 2
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
        self.assertTrue(table.hand_can_start)
        self.assertFalse(table.hand_has_started)
        table.start_hand()
        self.assertTrue(table.hand_has_started)
        self.assertFalse(table.hand_can_start)
        self.assertEqual(table.street, Street.PREFLOP)
        self.assertEqual(table.pot.value, 800)
        self.assertEqual(table.players.bb_seat, 1)

    def test_set_max_players(self):
        table = Table()
        for pl in self.pl_list2:
            pl.sit(table)
        self.assertEqual(table.max_players, 6)
        table.set_max_players(9)
        self.assertEqual(table.max_players, 9)

    def test_estimated_players_remaining(self):
        table = Table()
        tournament = Tournament(
            level=Level(1, 1000), total_players=200, starting_stack=20000

        )
        table.add_tournament(tournament)
        for pl in self.pl_list2:
            pl.sit(table)
        self.assertEqual(table.estimated_players_remaining, 149)

    def test_action_fold(self):
        table = Table()
        table.add_tournament(self.tournament)
        for player in self.pl_list2:
            table.add_player(player)
        table.set_bb_seat(2)
        table.start_hand()
        self.assertFalse(table.players[3].played)
        self.assertFalse(table.players[3].folded)
        self.assertEqual(table.players[3].stack, 11450)
        self.assertEqual(table.players[3].to_call, 400)
        self.assertEqual(table.players[3].current_bet, 0)
        self.assertEqual(table.pot.value, 900)
        self.assertEqual(table.pot.highest_bet, 400)
        self.assertTrue(table.players[3].is_current_player)
        self.assertFalse(table.players[3].hand_stats.preflop.flag_vpip)
        self.assertFalse(table.players[3].has_initiative)
        action = FoldAction(table.current_player)
        action.play()
        self.assertFalse(table.players[3].has_initiative)
        self.assertTrue(table.players[3].played)
        self.assertTrue(table.players[3].folded)
        self.assertEqual(table.players[3].stack, 11450)
        self.assertEqual(table.players[3].to_call, 400)
        self.assertEqual(table.players[3].current_bet, 0)
        self.assertEqual(table.pot.value, 900)
        self.assertEqual(table.pot.highest_bet, 400)
        self.assertFalse(table.players[3].is_current_player)
        self.assertFalse(table.players[3].hand_stats.preflop.flag_vpip)

    def test_action_call(self):
        table = Table()
        table.add_tournament(self.tournament)
        for player in self.pl_list2:
            table.add_player(player)
        table.set_bb_seat(2)
        table.start_hand()
        self.assertEqual(table.cnt_bets, 1)
        self.assertEqual(table.cnt_calls, 0)
        self.assertFalse(table.is_opened)
        self.assertFalse(table.players[3].played)
        self.assertFalse(table.players[3].folded)
        self.assertEqual(table.players[3].stack, 11450)
        self.assertEqual(table.players[3].to_call, 400)
        self.assertEqual(table.players[3].current_bet, 0)
        self.assertEqual(table.pot.value, 900)
        self.assertEqual(table.pot.highest_bet, 400)
        self.assertTrue(table.players[3].is_current_player)
        self.assertFalse(table.players[3].hand_stats.preflop.flag_vpip)
        self.assertFalse(table.players[3].has_initiative)
        action = CallAction(table.current_player)
        action.play()
        self.assertEqual(table.cnt_bets, 1)
        self.assertEqual(table.cnt_calls, 1)
        self.assertTrue(table.is_opened)
        self.assertTrue(table.players[3].played)
        self.assertFalse(table.players[3].folded)
        self.assertEqual(table.players[3].stack, 11050)
        self.assertEqual(table.players[3].to_call, 0)
        self.assertEqual(table.players[3].current_bet, 400)
        self.assertEqual(table.pot.value, 1300)
        self.assertEqual(table.pot.highest_bet, 400)
        self.assertFalse(table.players[3].is_current_player)
        self.assertTrue(table.players[3].hand_stats.preflop.flag_vpip)
        self.assertFalse(table.players[3].has_initiative)

    def test_action_raise(self):
        table = Table()
        table.add_tournament(self.tournament)
        for player in self.pl_list2:
            table.add_player(player)
        table.set_bb_seat(2)
        table.start_hand()
        self.assertEqual(table.cnt_bets, 1)
        self.assertEqual(table.cnt_calls, 0)
        self.assertFalse(table.is_opened)
        self.assertFalse(table.players[3].played)
        self.assertFalse(table.players[3].folded)
        self.assertEqual(table.players[3].stack, 11450)
        self.assertEqual(table.players[3].to_call, 400)
        self.assertEqual(table.players[3].current_bet, 0)
        self.assertEqual(table.pot.value, 900)
        self.assertEqual(table.pot.highest_bet, 400)
        self.assertTrue(table.players[3].is_current_player)
        self.assertFalse(table.players[3].hand_stats.preflop.flag_vpip)
        self.assertFalse(table.players[3].has_initiative)
        self.assertEqual(table.min_bet, 800)
        self.assertEqual(table.players[3].min_raise, 400)
        with self.assertRaises(NotSufficientRaiseError):
            action = RaiseAction(table.current_player, 300)
            action.play()
        self.assertEqual(table.min_bet, 800)
        self.assertEqual(table.players[3].min_raise, 400)
        action = RaiseAction(table.current_player, 1050)
        action.play()
        self.assertEqual(table.cnt_bets, 2)
        self.assertEqual(table.cnt_calls, 0)
        self.assertTrue(table.is_opened)
        self.assertTrue(table.players[3].played)
        self.assertFalse(table.players[3].folded)
        self.assertEqual(table.players[3].stack, 10000)
        self.assertEqual(table.players[3].to_call, 0)
        self.assertEqual(table.players[3].current_bet, 1450)
        self.assertEqual(table.pot.value, 2350)
        self.assertEqual(table.pot.highest_bet, 1450)
        self.assertFalse(table.players[3].is_current_player)
        self.assertTrue(table.players[3].hand_stats.preflop.flag_vpip)
        self.assertTrue(table.players[3].has_initiative)
        self.assertTrue(table.players[4].is_current_player)
        with self.assertRaises(NotSufficientRaiseError):
            action = RaiseAction(table.current_player, 1000)
            action.play()

    def test_action_check(self):
        table = Table()
        table.add_tournament(self.tournament)
        for player in self.pl_list2:
            table.add_player(player)
        table.set_bb_seat(2)
        table.start_hand()
        action = CallAction(table.current_player)
        action.play()

        action = FoldAction(table.current_player)
        action.play()
        action = FoldAction(table.current_player)
        action.play()
        action = FoldAction(table.current_player)
        action.play()
        action = FoldAction(table.current_player)
        action.play()
        self.assertFalse(table.players[2].played)
        self.assertFalse(table.players[2].folded)
        self.assertEqual(table.players[2].stack, 2050.0)
        self.assertEqual(table.players[2].to_call, 0)
        self.assertEqual(table.players[2].current_bet, 400)
        self.assertEqual(table.pot.value, 1300)
        self.assertEqual(table.pot.highest_bet, 400)
        self.assertTrue(table.players[2].is_current_player)
        action = CheckAction(table.current_player)
        action.play()
        self.assertTrue(table.players[2].played)
        self.assertFalse(table.players[2].folded)
        self.assertEqual(table.players[2].stack, 2050.0)
        self.assertEqual(table.players[2].to_call, 0)
        self.assertEqual(table.players[3].current_bet, 400)
        self.assertEqual(table.pot.value, 1300)
        self.assertEqual(table.pot.highest_bet, 400)
        self.assertFalse(table.players[2].is_current_player)

    def test_hand_example(self):
        hand_id = "2612804708405870609-6-1672853787"
        datetime = "04-01-2023 17:36:27"
        game_type = "Tournament"
        buy_in = BuyIn(prize_pool=4.5, bounty=0.0, rake=0.5)
        level = Level(value=1, bb=200)
        tournament_name = "GUERILLA"
        tournament_id = "608341002"
        table_number = "016"
        total_players = 2525
        max_players = 6
        button_seat = 4
        p1 = TablePlayer(name="FrenchAAAA", seat=1, init_stack=19575.0, bounty=2.25)
        p2 = TablePlayer(name="daifwa", seat=2, init_stack=21830.0, bounty=2.25)
        p3 = TablePlayer(name="Roomxx", seat=3, init_stack=34263.0, bounty=3.37)
        p4 = TablePlayer(name="SB Warrior34", seat=4, init_stack=18548.0, bounty=2.25)
        p5 = TablePlayer(name="GoToVG", seat=5, init_stack=26609.0, bounty=2.25)
        p6 = TablePlayer(name="manggy94", seat=6, init_stack=19175.0, bounty=2.25)
        players_list = [p1, p2, p3, p4, p5, p6]
        tournament = Tournament(
            level=level, name=tournament_name, id=tournament_id, buy_in=buy_in, total_players=total_players
        )
        table = Table(max_players=max_players)
        table.add_tournament(tournament)
        for player in players_list:
            table.add_player(player)
        bb_seat = table.players.get_bb_seat_from_button(button_seat)
        table.set_bb_seat(bb_seat)
        table.distribute_hero_cards("manggy94", "2c", "5h")
        table.start_hand()
        self.assertEqual(table.estimated_players_remaining, 2164)
        self.assertEqual(table.average_stack_bb, 116.67)
        self.assertEqual(table.min_bet, 400)
        self.assertEqual(table.min_bet_bb, 2)
        self.assertEqual(table.pot_value, 450)
        self.assertEqual(table.pot.highest_bet, 200)
        self.assertEqual(table.current_player.name, "FrenchAAAA")
        self.assertEqual(table.current_player.preflop_bet_amounts, [400, 440, 500, 600, 800, 1400, 2000, 19550.0])
        action = FoldAction(table.current_player)
        action.play()
        with self.assertRaises(ShowdownNotReachedError):
            table.current_player.shows("AsAd")
        self.assertEqual(table.pot_value, 450)
        self.assertEqual(table.pot.highest_bet, 200)
        self.assertEqual(table.current_player.name, "daifwa")
        action = CallAction(table.current_player)
        action.play()
        self.assertEqual(table.pot_value, 650)
        self.assertEqual(table.pot.highest_bet, 200)
        self.assertEqual(table.current_player.name, "Roomxx")
        action = FoldAction(table.current_player)
        action.play()
        self.assertEqual(table.pot_value, 650)
        self.assertEqual(table.pot.highest_bet, 200)
        self.assertEqual(table.current_player.name, "SB Warrior34")
        action = CallAction(table.current_player)
        action.play()
        self.assertEqual(table.pot_value, 850)
        self.assertEqual(table.pot.highest_bet, 200)
        self.assertEqual(table.current_player.name, "GoToVG")
        self.assertEqual(table.min_bet, 400)
        action = RaiseAction(table.current_player, 700)
        action.play()
        self.assertEqual(table.min_bet, 1400)
        self.assertEqual(table.pot_value, 1650)
        self.assertEqual(table.pot.highest_bet, 900)
        self.assertEqual(table.current_player.name, "manggy94")
        self.assertEqual(table.current_player.preflop_bet_amounts, [1400, 1540, 1750, 2100, 2800, 4900, 7000, 18950.0])
        action = FoldAction(table.current_player)
        action.play()
        self.assertEqual(table.pot_value, 1650)
        self.assertEqual(table.pot.highest_bet, 900)
        self.assertEqual(table.current_player.name, "daifwa")
        self.assertEqual(table.current_player.to_call, 700)
        action = CallAction(table.current_player)
        action.play()
        self.assertFalse(table.street_ended)
        self.assertFalse(table.hand_ended)
        self.assertFalse(table.next_hand_ready)
        self.assertEqual(table.pot_value, 2350)
        self.assertEqual(table.pot.highest_bet, 900)
        self.assertEqual(table.current_player.name, "SB Warrior34")
        action = CallAction(table.current_player)
        action.play()
        self.assertEqual(table.pot_value, 3050)
        self.assertEqual(table.pot.highest_bet, 900)
        self.assertTrue(table.street_ended)
        self.assertFalse(table.hand_ended)
        table.execute_flop("7h", "2d", "5c")
        self.assertEqual(table.board.len, 3)
        self.assertEqual(table.street, Street.FLOP)
        self.assertEqual(table.current_player.name, "GoToVG")
        self.assertEqual(table.current_player.postflop_bets,
                         [{'text': 'Min Bet', 'value': 200},
                          {'text': '1/4 Pot', 'value': 762},
                          {'text': '1/3 Pot', 'value': 1017},
                          {'text': '1/2 Pot', 'value': 1525},
                          {'text': '2/3 Pot', 'value': 2033},
                          {'text': '3/4 Pot', 'value': 2288},
                          {'text': 'Pot', 'value': 3050},
                          {'text': 'All-in', 'value': 25684.0}]
                         )
        self.assertEqual(table.nb_in_game, 3)
        self.assertEqual(table.seats_playing, [5, 2, 4])
        action = CheckAction(table.current_player)
        action.play()
        action = CheckAction(table.current_player)
        action.play()
        action = CheckAction(table.current_player)
        action.play()
        self.assertTrue(table.next_street_ready)
        with self.assertRaises(ValueError):
            table.execute_flop("7h", "2d", "5c")
        with self.assertRaises(ValueError):
            table.execute_river("8c")
        table.execute_turn("2h")
        self.assertEqual(table.board.len, 4)
        self.assertEqual(table.street, Street.TURN)
        self.assertEqual(table.current_player.name, "GoToVG")
        self.assertEqual(table.nb_in_game, 3)
        self.assertEqual(table.min_bet, 200)
        self.assertEqual(table.current_player.postflop_bets,
                         [{'text': 'Min Bet', 'value': 200},
                          {'text': '1/4 Pot', 'value': 762},
                          {'text': '1/3 Pot', 'value': 1017},
                          {'text': '1/2 Pot', 'value': 1525},
                          {'text': '2/3 Pot', 'value': 2033},
                          {'text': '3/4 Pot', 'value': 2288},
                          {'text': 'Pot', 'value': 3050},
                          {'text': 'All-in', 'value': 25684.0}]
                         )
        action = BetAction(table.current_player, 1000)
        action.play()
        self.assertEqual(table.min_bet, 2000)
        self.assertEqual(table.current_player.postflop_bets,
                         [{'text': 'Min Bet', 'value': 2000.0},
                          {'text': '1/2 Pot', 'value': 2025},
                          {'text': '2/3 Pot', 'value': 2700},
                          {'text': '3/4 Pot', 'value': 3038},
                          {'text': 'Pot', 'value': 4050},
                          {'text': 'All-in', 'value': 20905.0}]
                         )
        action = FoldAction(table.current_player)
        action.play()
        action = CallAction(table.current_player)
        action.play()
        self.assertTrue(table.street_ended)
        self.assertEqual(table.pot_value, 5050)
        self.assertEqual(table.pot.highest_bet, 1000)
        with self.assertRaises(ValueError):
            table.execute_turn("2h")
        table.execute_river("8c")
        self.assertEqual(table.board.len, 5)
        self.assertEqual(table.street, Street.RIVER)
        self.assertEqual(table.current_player.name, "GoToVG")
        self.assertEqual(table.nb_in_game, 2)
        self.assertEqual(table.current_player.postflop_bets,
                         [{'text': 'Min Bet', 'value': 200},
                          {'text': '1/4 Pot', 'value': 1262},
                          {'text': '1/3 Pot', 'value': 1683},
                          {'text': '1/2 Pot', 'value': 2525},
                          {'text': '2/3 Pot', 'value': 3367},
                          {'text': '3/4 Pot', 'value': 3788},
                          {'text': 'Pot', 'value': 5050},
                          {'text': 'All-in', 'value': 24684.0}]
                         )
        with self.assertRaises(NotSufficientBetError):
            action = BetAction(table.current_player, 100)
            action.play()
        action = BetAction(table.current_player, 2525)
        action.play()
        self.assertFalse(table.street_ended)
        with self.assertRaises(CannotParseWinnersError):
            table.calculate_and_distribute_rewards()
        self.assertEqual(table.current_player.postflop_bets,
                         [{'text': 'Min Bet', 'value': 5050.0},
                          {'text': '3/4 Pot', 'value': 5681},
                          {'text': 'Pot', 'value': 7575},
                          {'text': 'All-in', 'value': 16623.0}]
                         )
        action = FoldAction(table.current_player)
        action.play()
        self.assertEqual(table.pot_value, 7575)
        self.assertEqual(table.pot_value_bb, 37.88)

        self.assertTrue(table.street_ended)
        self.assertTrue(table.hand_ended)
        self.assertFalse(table.next_street_ready)
        self.assertTrue(table.next_hand_ready)
        self.assertEqual(table.players[5].init_stack - table.players[5].invested + table.pot_value, 29734.0)
        self.assertEqual(sum(pl.invested for pl in table.players), 7575)
        with self.assertRaises(ValueError):
            table.advance_to_showdown()
        table.calculate_and_distribute_rewards()
        self.assertEqual(table.pot_value, 0)
        self.assertEqual(table.players[1].stack, 19550.0)
        self.assertEqual(table.players[2].stack, 20905.0)
        self.assertEqual(table.players[3].stack, 34238.0)
        self.assertEqual(table.players[4].stack, 16623.0)
        self.assertEqual(table.players[5].stack, 29734.0)
        self.assertEqual(table.players[6].stack, 18950.0)
        table.advance_to_next_hand()
        self.assertEqual(table.pot_value, 0)
        self.assertEqual(table.pot_value_bb, 0)
        self.assertFalse(table.hand_has_started)
        self.assertTrue(table.hand_can_start)

    def test_hand_example_PLD(self):
        hand_id = "2113338189845364845-10-1634495793"
        datetime = "17-10-2021 18:36:33"
        game_type = "Tournament"
        total_players =3137
        buy_in = BuyIn(prize_pool=4.5, bounty=0.0, rake=0.5)
        level = Level(value=1, bb=200)
        tournament_name = "POUR LA DARONNE"
        tournament_id = "492049891"
        table_number = "0108"
        max_players = 6
        button_seat = 2
        p1 = TablePlayer(name="LASYLVE34", seat=1, init_stack=19625.0)
        p2 = TablePlayer(name="NotBadRiverr", seat=2, init_stack=17358.0)
        p3 = TablePlayer(name="Sofia1712", seat=3, init_stack=20175.0)
        p4 = TablePlayer(name="KassRM", seat=4, init_stack=12554.0)
        p5 = TablePlayer(name="Romain miklo", seat=5, init_stack=21200.0)
        p6 = TablePlayer(name="manggy94", seat=6, init_stack=29538.0)
        players_list = [p1, p2, p3, p4, p5, p6]
        tournament = Tournament(
            level=level,
            name=tournament_name,
            id=tournament_id,
            buy_in=buy_in,
            total_players=total_players
        )
        table = Table(max_players=max_players)
        table.add_tournament(tournament)
        for player in players_list:
            table.add_player(player)
        bb_seat = table.players.get_bb_seat_from_button(button_seat)
        table.set_bb_seat(bb_seat)
        table.distribute_hero_cards("manggy94", "2c", "Qd")
        table.start_hand()
        self.assertEqual(table.estimated_players_remaining, 3125)
        action = RaiseAction(table.current_player, 300)
        action.play()
        action = FoldAction(table.current_player)
        action.play()
        action = FoldAction(table.current_player)
        action.play()
        action = CallAction(table.current_player)
        action.play()
        action = FoldAction(table.current_player)
        action.play()
        action = CallAction(table.current_player)
        action.play()
        table.execute_flop("Jh", "5h", "2d")
        action = CheckAction(table.current_player)
        action.play()
        action = CheckAction(table.current_player)
        action.play()
        action = CheckAction(table.current_player)
        action.play()
        table.execute_turn("Tc")
        action = CheckAction(table.current_player)
        action.play()
        action = CheckAction(table.current_player)
        action.play()
        action = CheckAction(table.current_player)
        action.play()
        table.execute_river("8c")
        action = CheckAction(table.current_player)
        action.play()
        action = CheckAction(table.current_player)
        action.play()
        action = CheckAction(table.current_player)
        action.play()
        self.assertTrue(table.street_ended)
        table.advance_to_showdown()
        self.assertFalse(table.street_ended)
        self.assertTrue(table.hand_ended)
        self.assertFalse(table.can_parse_winners)
        table.players["NotBadRiverr"].shows("KcQh")
        self.assertFalse(table.can_parse_winners)
        table.players["KassRM"].shows("Ad8d")
        self.assertFalse(table.can_parse_winners)
        table.players["Romain miklo"].shows("4c4h")
        self.assertTrue(table.can_parse_winners)
        table.calculate_and_distribute_rewards()


if __name__ == '__main__':
    unittest.main()
