import unittest
import components.card as card


class MyRankTestCase(unittest.TestCase):

    def test_rank_order(self):
        self.assertGreater(card.Rank("5"), card.Rank("2"))
        self.assertLess(card.Rank("3"), card.Rank("A"))
        self.assertLess(card.Rank("K"), card.Rank("A"))
        self.assertLess(card.Rank("K"), card.Rank(1))

    def test_rank_conversion(self):
        self.assertEqual(card.Rank(1), card.Rank("A"))
        self.assertEqual(card.Rank("T"), card.Rank.TEN)
        self.assertEqual(card.Rank(10), card.Rank("T"))

    def test_rank_equality(self):
        self.assertEqual(card.Rank.NINE, card.Rank.NINE)
        self.assertNotEqual(card.Rank(10), card.Rank(1))

    def test_rank_difference(self):
        self.assertEqual(card.Rank.difference(card.Rank.NINE, card.Rank.SEVEN), 2)

    def test_magic_rank_difference(self):
        self.assertEqual(card.Rank.NINE - card.Rank.SEVEN, 2)
        self.assertEqual(card.Rank.ACE - card.Rank.SEVEN, 6)
        self.assertEqual(card.Rank.ACE - card.Rank.EIGHT, 6)
        self.assertEqual(card.Rank.KING - card.Rank.THREE, 10)
        self.assertEqual(card.Rank.ACE - card.Rank.THREE, 2)
        self.assertEqual(card.Rank.FIVE - card.Rank.JACK, 6)

    def test_magic_order(self):
        self.assertTrue(card.Rank.NINE > card.Rank.SIX)
        self.assertFalse(card.Rank.NINE > card.Rank.KING)

    def test_face_ranks(self):
        self.assertIn(card.Rank.KING, card.FACE_RANKS)
        self.assertIn(card.Rank.QUEEN, card.FACE_RANKS)
        self.assertIn(card.Rank.JACK, card.FACE_RANKS)


if __name__ == '__main__':
    unittest.main()
