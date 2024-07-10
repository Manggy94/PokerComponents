import unittest
from pkrcomponents.components.tournaments.buy_in import BuyIn


class BuyInTest(unittest.TestCase):

    def setUp(self):
        self.buyin = BuyIn(prize_pool=10.0, bounty=5.0, rake=1.0)

    def test_invalid_prize_pool_raises_error(self):
        with self.assertRaises(ValueError):
            self.buyin.prize_pool = -1

    def test_invalid_bounty_raises_error(self):
        with self.assertRaises(ValueError):
            self.buyin.bounty = -1

    def test_invalid_rake_raises_error(self):
        with self.assertRaises(ValueError):
            self.buyin.rake = -1

    def test_valid_prize_pool_sets_correctly(self):
        self.buyin.prize_pool = 20.0
        self.assertEqual(self.buyin.prize_pool, 20.0)

    def test_valid_bounty_sets_correctly(self):
        self.buyin.bounty = 10.0
        self.assertEqual(self.buyin.bounty, 10.0)

    def test_valid_rake_sets_correctly(self):
        self.buyin.rake = 2.0
        self.assertEqual(self.buyin.rake, 2.0)

    def test_total_calculated_correctly(self):
        self.assertEqual(self.buyin.total, 16.0)

    def test_to_json_returns_correct_dict(self):
        self.assertEqual(self.buyin.to_json(), {"prize_pool": 10.0, "bounty": 5.0, "rake": 1.0})
