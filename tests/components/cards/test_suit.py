import unittest
from pkrcomponents.components.cards.suit import Suit


class MySuitTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.all_suits = list(Suit)

    def test_name(self):
        self.assertEqual(Suit("c").name, "CLUBS")
        self.assertEqual(Suit("d").name, "DIAMONDS")
        self.assertEqual(Suit("h").name, "HEARTS")
        self.assertEqual(Suit("s").name, "SPADES")

    def test_symbol(self):
        self.assertEqual(Suit("c").symbol, "♣")
        self.assertEqual(Suit("d").symbol, "♦")
        self.assertEqual(Suit("h").symbol, "♥")
        self.assertEqual(Suit("s").symbol, "♠")

    def test_suits_length(self):
        self.assertEqual(len(self.all_suits), 4)

    def test_suits_contains(self):
        all_suits = list(Suit)
        self.assertIn(Suit("c"), all_suits)
        self.assertIn(Suit("d"), all_suits)
        self.assertIn(Suit("h"), all_suits)
        self.assertIn(Suit("s"), all_suits)

    def test_suit_conversion(self):
        self.assertIsInstance(repr(self.all_suits[0]), str)
        self.assertIsInstance(str(self.all_suits[0]), str)
        self.assertEqual(str(self.all_suits[0]), "c")
        self.assertEqual(str(self.all_suits[1]), "d")
        self.assertEqual(str(self.all_suits[2]), "h")
        self.assertEqual(str(self.all_suits[3]), "s")
        self.assertEqual(Suit("c"), Suit("clubs"))
        self.assertEqual(Suit("s"), Suit("SPADES"))
        self.assertEqual(Suit("d"), Suit("DIAMONDS"))
        self.assertEqual(Suit("h"), Suit("HEARTS"))
        self.assertEqual(Suit("CLUBS"), Suit("clubs"))
        
    def test_suits_combinations(self):
        self.assertIsInstance(Suit.get_suit_combinations(), tuple)
        self.assertIsInstance(Suit.get_paired_suit_combinations(), tuple)
        self.assertIsInstance(Suit.get_suited_suit_combinations(), tuple)
        self.assertIsInstance(Suit.get_offsuit_suit_combinations(), tuple)
        self.assertEqual(len(Suit.get_suit_combinations()), 16)
        self.assertEqual(len(Suit.get_paired_suit_combinations()), 6)
        self.assertEqual(len(Suit.get_suited_suit_combinations()), 4)
        self.assertEqual(len(Suit.get_offsuit_suit_combinations()), 12)


if __name__ == '__main__':
    unittest.main()
