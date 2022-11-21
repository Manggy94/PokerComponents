import unittest

import numpy

import pkrcomponents.listings as lst


class MyListingsTestCase(unittest.TestCase):
    def test_listings(self):
        self.assertIsInstance(lst.all_actions, numpy.ndarray)
        self.assertEqual(lst.all_actions.size, 10)
        self.assertIsInstance(lst.all_cards, numpy.ndarray)
        self.assertEqual(lst.all_cards.size, 52)
        self.assertIsInstance(lst.all_combos, numpy.ndarray)
        self.assertEqual(lst.all_combos.size, 1326)
        self.assertIsInstance(lst.all_hands, numpy.ndarray)
        self.assertEqual(lst.all_hands.size, 169)


if __name__ == '__main__':
    unittest.main()
