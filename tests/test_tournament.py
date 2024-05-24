import unittest
from pkrcomponents.tournament import Tournament, Buyin, Level, Payout, Payouts
from pkrcomponents.constants import MoneyType


class MyTournamentTestCase(unittest.TestCase):

    def setUp(self):
        self.buyin = Buyin(freeze=9, ko=0, rake=1)
        self.tour = Tournament("tour_id", name="PLD", money_type="real", buyin=self.buyin)
        self.level = Level()
        self.level2 = Level(level=4, bb=600)

    def test_new_tournament(self):
        tour = Tournament(level=self.level)
        self.assertIsInstance(tour, Tournament)
        self.assertIsInstance(tour.level, Level)
        self.assertEqual(tour.id, "0000")
        self.assertEqual(tour.name, "Kill The Fish")
        self.assertTrue(tour.is_ko)
        tour.is_ko = False
        self.assertFalse(tour.is_ko)
        tour.level = self.level2

    def test_str(self):
        self.assertIsInstance(self.tour.__str__(), str)

    def test_id_and_type(self):
        self.assertIsInstance(self.tour.id, str)
        self.assertEqual(self.tour.id, "tour_id")
        self.tour.id = "None"
        self.assertEqual(self.tour.id, "None")
        self.assertIsInstance(self.tour.money_type, MoneyType)
        self.assertEqual(self.tour.money_type, MoneyType.REAL)
        self.tour.money_type = "play"
        self.assertEqual(self.tour.money_type, MoneyType.PLAY)

    def test_name(self):
        self.assertIsInstance(self.tour.name, str)
        self.assertEqual(self.tour.name, "PLD")
        self.tour.name = "Name"
        self.assertEqual(self.tour.name, "Name")

    def test_buyin(self):
        self.assertIsInstance(self.tour.buyin, Buyin)
        self.assertEqual(self.tour.buyin.freeze_part, 9)
        self.assertEqual(self.tour.buyin.ko_part, 0)
        self.assertEqual(self.tour.buyin.rake, 1)
        self.assertEqual(self.tour.buyin.total, 10)
        self.tour.buyin = Buyin.from_total(20)
        self.assertEqual(self.tour.buyin.freeze_part, 9)
        self.assertEqual(self.tour.buyin.ko_part, 9)
        self.assertEqual(self.tour.buyin.rake, 2)

    def test_to_json(self):
        self.assertIsInstance(self.tour.to_json(), dict)
        self.assertEqual(self.tour.to_json(), {
            'level': {
                'level': 1,
                'ante': 25.0,
                'sb': 100.0,
                'bb': 200.0
            },
            'id': 'tour_id',
            'name': 'PLD',
            'buy_in': {'freeze': 9, 'ko': 0, 'rake': 1},
            'is_ko': True,
            'money_type': MoneyType('Real money')})


class TestTournament(unittest.TestCase):

    def setUp(self):
        self.buyin = Buyin(freeze=9, ko=0, rake=1)
        self.level = Level(level=4, bb=600)
        self.tour = Tournament("tour_id", name="PLD", money_type="real", buyin=self.buyin, level=self.level)

    def test_invalid_money_type_raises_error(self):
        with self.assertRaises(ValueError):
            self.tour.money_type = "invalid"

    def test_invalid_starting_stack_raises_error(self):
        with self.assertRaises(ValueError):
            self.tour.starting_stack = -1

    def test_invalid_total_players_raises_error(self):
        with self.assertRaises(ValueError):
            self.tour.total_players = -1

    def test_invalid_players_remaining_raises_error(self):
        self.tour.total_players = 100
        with self.assertRaises(ValueError):
            self.tour.players_remaining = -1
        with self.assertRaises(ValueError):
            self.tour.players_remaining = 101

    def test_valid_buyin_sets_correctly(self):
        self.tour.buyin = Buyin(freeze=10, ko=0, rake=1)
        self.assertEqual(self.tour.buyin.total, 11)

    def test_valid_level_sets_correctly(self):
        self.tour.level = Level(level=5, bb=800)
        self.assertEqual(self.tour.level.bb, 800)

    def test_valid_money_type_sets_correctly(self):
        self.tour.money_type = "play"
        self.assertEqual(self.tour.money_type, MoneyType.PLAY)

    def test_valid_starting_stack_sets_correctly(self):
        self.tour.starting_stack = 30000
        self.assertEqual(self.tour.starting_stack, 30000)

    def test_valid_total_players_sets_correctly(self):
        self.tour.total_players = 100
        self.assertEqual(self.tour.total_players, 100)

    def test_valid_players_remaining_sets_correctly(self):
        self.tour.total_players = 100
        self.tour.players_remaining = 50
        self.assertEqual(self.tour.players_remaining, 50)

    def test_total_chips_calculated_correctly(self):
        self.tour.total_players = 100
        self.tour.starting_stack = 20000
        self.assertEqual(self.tour.total_chips, 2000000)

    def test_average_stack_calculated_correctly(self):
        self.tour.total_players = 100
        self.tour.players_remaining = 50
        self.tour.starting_stack = 20000
        self.assertEqual(self.tour.average_stack, 40000)

    def test_players_eliminated_calculated_correctly(self):
        self.tour.total_players = 100
        self.tour.players_remaining = 50
        self.assertEqual(self.tour.players_eliminated, 50)

    def test_tournament_progression_calculated_correctly(self):
        self.tour.total_players = 100
        self.tour.players_remaining = 50
        self.assertEqual(self.tour.tournament_progression, 50/99)

    def test_next_tier_calculated_correctly(self):
        self.tour.total_players = 100
        self.tour.players_remaining = 50
        self.tour.payouts = Payouts([Payout(1, 300.0), Payout(2, 200.0), Payout(3, 100.0)])
        self.assertEqual(self.tour.next_tier, 3)

    def test_next_reward_calculated_correctly(self):
        self.tour.total_players = 100
        self.tour.players_remaining = 50
        self.tour.payouts = Payouts([Payout(1, 300.0), Payout(2, 200.0), Payout(3, 100.0)])
        self.assertEqual(self.tour.next_reward, 100.0)

    def test_players_to_next_tier_calculated_correctly(self):
        self.tour.total_players = 100
        self.tour.players_remaining = 50
        self.tour.payouts = Payouts([Payout(1, 300.0), Payout(2, 200.0), Payout(3, 100.0)])
        self.assertEqual(self.tour.players_to_next_tier, 47)


if __name__ == '__main__':
    unittest.main()
