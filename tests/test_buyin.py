import unittest
from pkrcomponents.tournament import Buyin


class BuyinTestCase(unittest.TestCase):

    def setUp(self):
        self.buyin = Buyin(freeze=9, ko=0, rake=1)

    def test_invalid_freeze_part_raises_error(self):
        with self.assertRaises(ValueError):
            self.buyin.freeze_part = -1

    def test_invalid_ko_part_raises_error(self):
        with self.assertRaises(ValueError):
            self.buyin.ko_part = -1

    def test_invalid_rake_raises_error(self):
        with self.assertRaises(ValueError):
            self.buyin.rake = -1

    def test_valid_freeze_part_sets_correctly(self):
        self.buyin.freeze_part = 10
        self.assertEqual(self.buyin.freeze_part, 10)

    def test_valid_ko_part_sets_correctly(self):
        self.buyin.ko_part = 10
        self.assertEqual(self.buyin.ko_part, 10)

    def test_valid_rake_sets_correctly(self):
        self.buyin.rake = 2
        self.assertEqual(self.buyin.rake, 2)

    def test_total_calculated_correctly(self):
        self.assertEqual(self.buyin.total, 10)

    def test_from_total_sets_correctly(self):
        new_buyin = Buyin.from_total(20)
        self.assertEqual(new_buyin.freeze_part, 9)
        self.assertEqual(new_buyin.ko_part, 9)
        self.assertEqual(new_buyin.rake, 2)

    def test_to_json_returns_correct_dict(self):
        self.assertEqual(self.buyin.to_json(), {"freeze": 9, "ko": 0, "rake": 1})