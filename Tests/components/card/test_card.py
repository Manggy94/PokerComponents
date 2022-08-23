import unittest
import components.card as card


class MyTestCase(unittest.TestCase):

    def test_suits_length(self):
        all_suits = list(card.Suit)
        self.assertEqual(len(all_suits), 4)

    def test_suits_contains(self):
        all_suits = list(card.Suit)
        self.assertIn(card.Suit("c"), all_suits)
        self.assertIn(card.Suit("d"), all_suits)
        self.assertIn(card.Suit("h"), all_suits)
        self.assertIn(card.Suit("s"), all_suits)




if __name__ == '__main__':
    unittest.main()
