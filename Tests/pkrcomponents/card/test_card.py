import unittest
import pkrcomponents.card as card


class MyCardTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.all_cards = list(card.Card)

    def test_new(self):
        with self.assertRaises(ValueError):
            card.Card("As3")

    def test_cards_length(self):
        self.assertEqual(len(self.all_cards), 52)

    def test_make_random(self):
        new_card = card.Card.make_random()
        self.assertIsInstance(new_card, card.Card)

    def test_card_slots(self):
        new_card = card.Card.make_random()
        self.assertIsInstance(new_card.rank, card.Rank)
        self.assertIsInstance(new_card.suit, card.Suit)

    def test_card_rank(self):
        new_card = card.Card("As")
        self.assertEqual(new_card.rank, card.Rank.ACE)
        self.assertEqual(new_card.suit, card.Suit.SPADES)
        self.assertNotEqual(new_card.rank, card.Rank.TEN)
        self.assertNotEqual(new_card.suit, card.Suit.HEARTS)

    def test_card_difference_operator(self):
        c1 = card.Card("Ah")
        c2 = card.Card("As")
        c3 = card.Card("Th")
        c4 = card.Card("4d")
        self.assertEqual(c1 - c2, 0)
        self.assertEqual(c1 - c3, 4)
        self.assertEqual(c3 - c1, 4)
        self.assertEqual(c1 - c4, 3)
        self.assertEqual(c3 - c4, 6)
        with self.assertRaises(ValueError):
            c1 == 3
        with self.assertRaises(ValueError):
            c1 < 3

    def test_is_face(self):
        self.assertTrue(card.Card("Ks").is_face)
        self.assertFalse(card.Card("As").is_face)
        self.assertFalse(card.Card("Ts").is_face)
        self.assertFalse(card.Card("4h").is_face)

    def test_is_broadway(self):
        self.assertTrue(card.Card("Ks").is_broadway)
        self.assertTrue(card.Card("As").is_broadway)
        self.assertTrue(card.Card("Ts").is_broadway)
        self.assertFalse(card.Card("4h").is_broadway)


if __name__ == '__main__':
    unittest.main()
