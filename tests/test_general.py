import unittest
import pkrcomponents.hand as hand


class MyGeneralTestCase(unittest.TestCase):

    def test_suits_combinations(self):
        self.assertIsInstance(hand._PAIR_SUIT_COMBINATIONS, tuple)
        self.assertIsInstance(hand._SUITED_SUIT_COMBINATIONS, tuple)
        self.assertIsInstance(hand._OFFSUIT_SUIT_COMBINATIONS, tuple)
        self.assertEqual(len(hand._PAIR_SUIT_COMBINATIONS), 6)
        self.assertEqual(len(hand._SUITED_SUIT_COMBINATIONS), 4)
        self.assertEqual(len(hand._OFFSUIT_SUIT_COMBINATIONS), 12)

    def test_pair_hands(self):
        self.assertIsInstance(hand.PAIR_HANDS, tuple)
        self.assertEqual(len(hand.PAIR_HANDS), 13)

    def test_offsuit_hands(self):
        self.assertIsInstance(hand.OFFSUIT_HANDS, tuple)
        self.assertEqual(len(hand.OFFSUIT_HANDS), 78)

    def test_suited_hands(self):
        self.assertIsInstance(hand.SUITED_HANDS, tuple)
        self.assertEqual(len(hand.SUITED_HANDS), 78)


if __name__ == '__main__':
    unittest.main()
