import unittest
from pkrcomponents.components.cards import BROADWAY_RANKS, FACE_RANKS, Rank


class MyRankTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.all_ranks = list(Rank)

    def test_ranks_length(self):
        self.assertEqual(len(self.all_ranks), 13)

    def test_symbol(self):
        self.assertEqual(Rank.ACE.symbol, "A")
        self.assertEqual(Rank.DEUCE.symbol, "2")
        self.assertEqual(Rank.THREE.symbol, "3")
        self.assertEqual(Rank.FOUR.symbol, "4")
        self.assertEqual(Rank.FIVE.symbol, "5")
        self.assertEqual(Rank.SIX.symbol, "6")
        self.assertEqual(Rank.SEVEN.symbol, "7")
        self.assertEqual(Rank.EIGHT.symbol, "8")
        self.assertEqual(Rank.NINE.symbol, "9")
        self.assertEqual(Rank.TEN.symbol, "T")
        self.assertEqual(Rank.JACK.symbol, "J")
        self.assertEqual(Rank.QUEEN.symbol, "Q")
        self.assertEqual(Rank.KING.symbol, "K")

    def test_ranks_contains(self):
        self.assertIn(Rank.ACE, self.all_ranks)
        self.assertIn(Rank.DEUCE, self.all_ranks)
        self.assertIn(Rank.THREE, self.all_ranks)
        self.assertIn(Rank.FOUR, self.all_ranks)
        self.assertIn(Rank.FIVE, self.all_ranks)
        self.assertIn(Rank.SIX, self.all_ranks)
        self.assertIn(Rank.SEVEN, self.all_ranks)
        self.assertIn(Rank.EIGHT, self.all_ranks)
        self.assertIn(Rank.NINE, self.all_ranks)
        self.assertIn(Rank.TEN, self.all_ranks)
        self.assertIn(Rank.JACK, self.all_ranks)
        self.assertIn(Rank.QUEEN, self.all_ranks)
        self.assertIn(Rank.KING, self.all_ranks)

    def test_rank_order(self):
        self.assertGreater(Rank("5"), Rank("2"))
        self.assertLess(Rank("3"), Rank("A"))
        self.assertLess(Rank("K"), Rank("A"))
        self.assertLess(Rank("K"), Rank(1))

    def test_rank_conversion(self):
        self.assertEqual(Rank(1), Rank("A"))
        self.assertEqual(Rank("T"), Rank.TEN)
        self.assertEqual(Rank(10), Rank("T"))

    def test_rank_equality(self):
        self.assertEqual(Rank.NINE, Rank.NINE)
        self.assertNotEqual(Rank(10), Rank(1))

    def test_rank_difference(self):
        self.assertEqual(
            Rank.difference(Rank.NINE, Rank.SEVEN), 2)

    def test_rank_difference_operator(self):
        self.assertEqual(Rank.NINE - Rank.SEVEN, 2)
        self.assertEqual(Rank.ACE - Rank.SEVEN, 6)
        self.assertEqual(Rank.ACE - Rank.EIGHT, 6)
        self.assertEqual(Rank.KING - Rank.THREE, 10)
        self.assertEqual(Rank.ACE - Rank.THREE, 2)
        self.assertEqual(Rank.FIVE - Rank.JACK, 6)

    def test_rank_order_operator(self):
        self.assertTrue(Rank.NINE > Rank.SIX)
        self.assertFalse(Rank.NINE > Rank.KING)

    def test_face_ranks(self):
        self.assertNotIn(Rank.TEN, FACE_RANKS)
        self.assertIn(Rank.KING, FACE_RANKS)
        self.assertIn(Rank.QUEEN, FACE_RANKS)
        self.assertIn(Rank.JACK, FACE_RANKS)

    def test_broadway_ranks(self):
        self.assertIn(Rank.TEN, BROADWAY_RANKS)
        self.assertIn(Rank.KING, BROADWAY_RANKS)
        self.assertIn(Rank.QUEEN, BROADWAY_RANKS)
        self.assertIn(Rank.JACK, BROADWAY_RANKS)
        self.assertIn(Rank.ACE, BROADWAY_RANKS)

    def test_is_broadway(self):
        self.assertTrue(Rank.ACE.is_broadway)
        self.assertTrue(Rank.KING.is_broadway)
        self.assertTrue(Rank.QUEEN.is_broadway)
        self.assertTrue(Rank.JACK.is_broadway)
        self.assertTrue(Rank.TEN.is_broadway)
        self.assertFalse(Rank.NINE.is_broadway)
        self.assertFalse(Rank.EIGHT.is_broadway)
        self.assertFalse(Rank.SEVEN.is_broadway)
        self.assertFalse(Rank.SIX.is_broadway)
        self.assertFalse(Rank.FIVE.is_broadway)
        self.assertFalse(Rank.FOUR.is_broadway)
        self.assertFalse(Rank.THREE.is_broadway)
        self.assertFalse(Rank.DEUCE.is_broadway)

    def test_is_face(self):
        self.assertTrue(Rank.KING.is_face)
        self.assertTrue(Rank.QUEEN.is_face)
        self.assertTrue(Rank.JACK.is_face)
        self.assertFalse(Rank.ACE.is_face)
        self.assertFalse(Rank.TEN.is_face)
        self.assertFalse(Rank.NINE.is_face)
        self.assertFalse(Rank.EIGHT.is_face)
        self.assertFalse(Rank.SEVEN.is_face)
        self.assertFalse(Rank.SIX.is_face)
        self.assertFalse(Rank.FIVE.is_face)
        self.assertFalse(Rank.FOUR.is_face)
        self.assertFalse(Rank.THREE.is_face)
        self.assertFalse(Rank.DEUCE.is_face)

    def test_short_name(self):
        self.assertEqual(Rank.ACE.short_name, "A")
        self.assertEqual(Rank.DEUCE.short_name, "2")
        self.assertEqual(Rank.THREE.short_name, "3")
        self.assertEqual(Rank.FOUR.short_name, "4")
        self.assertEqual(Rank.FIVE.short_name, "5")
        self.assertEqual(Rank.SIX.short_name, "6")
        self.assertEqual(Rank.SEVEN.short_name, "7")
        self.assertEqual(Rank.EIGHT.short_name, "8")
        self.assertEqual(Rank.NINE.short_name, "9")
        self.assertEqual(Rank.TEN.short_name, "T")
        self.assertEqual(Rank.JACK.short_name, "J")
        self.assertEqual(Rank.QUEEN.short_name, "Q")
        self.assertEqual(Rank.KING.short_name, "K")

    def test_str(self):
        self.assertEqual(str(Rank.ACE), "A")
        self.assertEqual(str(Rank.DEUCE), "2")
        self.assertEqual(str(Rank.THREE), "3")
        self.assertEqual(str(Rank.FOUR), "4")
        self.assertEqual(str(Rank.FIVE), "5")
        self.assertEqual(str(Rank.SIX), "6")
        self.assertEqual(str(Rank.SEVEN), "7")
        self.assertEqual(str(Rank.EIGHT), "8")
        self.assertEqual(str(Rank.NINE), "9")
        self.assertEqual(str(Rank.TEN), "T")
        self.assertEqual(str(Rank.JACK), "J")
        self.assertEqual(str(Rank.QUEEN), "Q")
        self.assertEqual(str(Rank.KING), "K")


if __name__ == '__main__':
    unittest.main()
