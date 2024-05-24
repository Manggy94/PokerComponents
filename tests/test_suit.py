import unittest
import pkrcomponents.card as card


class MySuitTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.all_suits = list(card.Suit)

    def test_suits_length(self):
        self.assertEqual(len(self.all_suits), 4)

    def test_suits_contains(self):
        all_suits = list(card.Suit)
        self.assertIn(card.Suit("c"), all_suits)
        self.assertIn(card.Suit("d"), all_suits)
        self.assertIn(card.Suit("h"), all_suits)
        self.assertIn(card.Suit("s"), all_suits)

    def test_suit_conversion(self):
        self.assertIsInstance(repr(self.all_suits[0]), str)
        self.assertIsInstance(str(self.all_suits[0]), str)
        self.assertEqual(str(self.all_suits[0]), "c")
        self.assertEqual(str(self.all_suits[1]), "d")
        self.assertEqual(str(self.all_suits[2]), "h")
        self.assertEqual(str(self.all_suits[3]), "s")
        self.assertEqual(card.Suit("c"), card.Suit("clubs"))
        self.assertEqual(card.Suit("s"), card.Suit("SPADES"))
        self.assertEqual(card.Suit("d"), card.Suit("DIAMONDS"))
        self.assertEqual(card.Suit("h"), card.Suit("HEARTS"))
        self.assertEqual(card.Suit("CLUBS"), card.Suit("clubs"))


if __name__ == '__main__':
    unittest.main()
