import unittest
from pkrcomponents.components.cards import Card, Rank, Suit
import pkrcomponents.components.cards.card as card
import pkrcomponents.components.cards.rank
import pkrcomponents.components.cards.suit


class MyCardTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.all_cards = list(Card)

    def test_name(self):
        self.assertEqual(Card("As").name, "ACE of SPADES")
        self.assertEqual(Card("Th").name, "TEN of HEARTS")
        self.assertEqual(Card("4d").name, "FOUR of DIAMONDS")
        self.assertEqual(Card("Kc").name, "KING of CLUBS")

    def test_symbol(self):
        self.assertEqual(Card("As").symbol, "A♠")
        self.assertEqual(Card("Th").symbol, "T♥")
        self.assertEqual(Card("4d").symbol, "4♦")
        self.assertEqual(Card("Kc").symbol, "K♣")

    def test_new(self):
        with self.assertRaises(ValueError):
            Card("As3")
        with self.assertRaises(TypeError):
            Card(8)

    def test_cards_length(self):
        self.assertEqual(len(self.all_cards), 52)

    def test_make_random(self):
        new_card = Card.make_random()
        self.assertIsInstance(new_card, Card)

    def test_card_slots(self):
        new_card = Card.make_random()
        self.assertIsInstance(new_card.rank, pkrcomponents.components.cards.rank.Rank)
        self.assertIsInstance(new_card.suit, pkrcomponents.components.cards.suit.Suit)

    def test_card_rank(self):
        new_card = Card("As")
        self.assertEqual(new_card.rank, pkrcomponents.components.cards.rank.Rank.ACE)
        self.assertEqual(new_card.suit, pkrcomponents.components.cards.suit.Suit.SPADES)
        self.assertNotEqual(new_card.rank, pkrcomponents.components.cards.rank.Rank.TEN)
        self.assertNotEqual(new_card.suit, pkrcomponents.components.cards.suit.Suit.HEARTS)

    def test_card_difference_operator(self):
        c1 = Card("Ah")
        c2 = Card("As")
        c3 = Card("Th")
        c4 = Card("4d")
        a = 3
        self.assertEqual(c1 - c2, 0)
        self.assertEqual(c1 - c3, 4)
        self.assertEqual(c3 - c1, 4)
        self.assertEqual(c1 - c4, 3)
        self.assertEqual(c3 - c4, 6)
        with self.assertRaises(ValueError):
            c1 == a
        with self.assertRaises(ValueError):
            c1 < a

    def test_is_face(self):
        self.assertTrue(Card("Ks").is_face)
        self.assertFalse(Card("As").is_face)
        self.assertFalse(Card("Ts").is_face)
        self.assertFalse(Card("4h").is_face)

    def test_is_broadway(self):
        self.assertTrue(Card("Ks").is_broadway)
        self.assertTrue(Card("As").is_broadway)
        self.assertTrue(Card("Ts").is_broadway)
        self.assertFalse(Card("4h").is_broadway)




if __name__ == '__main__':
    unittest.main()
