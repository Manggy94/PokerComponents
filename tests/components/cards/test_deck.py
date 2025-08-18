import unittest
from pkrcomponents.components.cards import Card
from pkrcomponents.components.cards import Deck

class MyDeckTestCase(unittest.TestCase):

    def test_new_deck(self):
        self.assertIsInstance(Deck(), Deck)
        self.assertEqual(Deck().cards, list(Card))
        self.assertEqual(len(Deck().cards), 52)

    def test_shuffle(self):
        deck = Deck()
        deck.shuffle()
        self.assertFalse(deck.cards[0:4] == [Card('2c'), Card('2d'), Card('2h'), Card('2s')])
        self.assertEqual(len(deck.cards), 52)

    def test_reset(self):
        deck = Deck()
        deck.cards.pop()
        deck.cards.pop()
        self.assertEqual(len(deck.cards), 50)
        deck.reset()
        self.assertEqual(len(deck.cards), 52)

    def test_draw(self):
        deck = Deck()
        c1 = deck.draw()
        self.assertIsInstance(c1, Card)
        self.assertEqual(len(deck.cards), 51)
        self.assertNotIn(c1, deck.cards)
        deck.reset()
        c2 = deck.draw("As")
        self.assertEqual(c2, Card("As"))
        self.assertNotIn(c2, deck.cards)
        self.assertEqual(len(deck.cards), 51)

    def test_to_json(self):
        self.assertIsInstance(Deck().to_json(), dict)
        self.assertIsInstance(Deck().to_json()["cards"], list)
        self.assertIsInstance(Deck().to_json()["len"], int)

    def test_replace(self):
        deck = Deck()
        c1 = deck.draw()
        deck.replace(c1)
        self.assertIn(c1, deck.cards)
        self.assertEqual(len(deck.cards), 52)
        c2 = deck.draw("As")
        deck.replace(c2)
        self.assertIn(c2, deck.cards)
        self.assertEqual(len(deck.cards), 52)


if __name__ == '__main__':
    unittest.main()
