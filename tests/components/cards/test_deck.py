import unittest
import pkrcomponents.components.cards.card as card
import pkrcomponents.components.cards.deck


class MyDeckTestCase(unittest.TestCase):

    def test_new_deck(self):
        self.assertIsInstance(pkrcomponents.components.cards.deck.Deck(), pkrcomponents.components.cards.deck.Deck)
        self.assertEqual(pkrcomponents.components.cards.deck.Deck().cards, list(card.Card))
        self.assertEqual(len(pkrcomponents.components.cards.deck.Deck().cards), 52)

    def test_shuffle(self):
        deck = pkrcomponents.components.cards.deck.Deck()
        deck.shuffle()
        self.assertFalse(deck.cards[0:4] == [card.Card('2c'), card.Card('2d'), card.Card('2h'), card.Card('2s')])
        self.assertEqual(len(deck.cards), 52)

    def test_reset(self):
        deck = pkrcomponents.components.cards.deck.Deck()
        deck.cards.pop()
        deck.cards.pop()
        self.assertEqual(len(deck.cards), 50)
        deck.reset()
        self.assertEqual(len(deck.cards), 52)

    def test_draw(self):
        deck = pkrcomponents.components.cards.deck.Deck()
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
        self.assertIsInstance(pkrcomponents.components.cards.deck.Deck().to_json(), dict)
        self.assertIsInstance(pkrcomponents.components.cards.deck.Deck().to_json()["cards"], list)
        self.assertIsInstance(pkrcomponents.components.cards.deck.Deck().to_json()["len"], int)

    def test_replace(self):
        deck = pkrcomponents.components.cards.deck.Deck()
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
