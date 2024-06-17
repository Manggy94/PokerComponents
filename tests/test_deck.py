import unittest
import pkrcomponents.cards.card as card
import pkrcomponents.deck


class MyDeckTestCase(unittest.TestCase):

    def test_new_deck(self):
        self.assertIsInstance(pkrcomponents.deck.Deck(), pkrcomponents.deck.Deck)
        self.assertEqual(pkrcomponents.deck.Deck().cards, list(card.Card))
        self.assertEqual(len(pkrcomponents.deck.Deck().cards), 52)

    def test_shuffle(self):
        deck = pkrcomponents.deck.Deck()
        deck.shuffle()
        self.assertFalse(deck.cards[0:4] == [card.Card('2c'), card.Card('2d'), card.Card('2h'), card.Card('2s')])
        self.assertEqual(len(deck.cards), 52)

    def test_reset(self):
        deck = pkrcomponents.deck.Deck()
        deck.cards.pop()
        deck.cards.pop()
        self.assertEqual(len(deck.cards), 50)
        deck.reset()
        self.assertEqual(len(deck.cards), 52)

    def test_draw(self):
        deck = pkrcomponents.deck.Deck()
        c1 = deck.draw()
        self.assertIsInstance(c1, card.Card)
        self.assertEqual(len(deck.cards), 51)
        self.assertNotIn(c1, deck.cards)
        deck.reset()
        c2 = deck.draw("As")
        self.assertEqual(c2, card.Card("As"))
        self.assertNotIn(c2, deck.cards)
        self.assertEqual(len(deck.cards), 51)

    def test_to_json(self):
        self.assertIsInstance(pkrcomponents.deck.Deck().to_json(), dict)
        self.assertIsInstance(pkrcomponents.deck.Deck().to_json()["cards"], list)
        self.assertIsInstance(pkrcomponents.deck.Deck().to_json()["len"], int)


if __name__ == '__main__':
    unittest.main()
