import unittest
import pkrcomponents.components.cards.rank


class MyRankTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.all_ranks = list(pkrcomponents.components.cards.rank.Rank)

    def test_ranks_length(self):
        self.assertEqual(len(self.all_ranks), 13)

    def test_symbol(self):
        self.assertEqual(pkrcomponents.components.cards.rank.Rank.ACE.symbol, "A")
        self.assertEqual(pkrcomponents.components.cards.rank.Rank.DEUCE.symbol, "2")
        self.assertEqual(pkrcomponents.components.cards.rank.Rank.THREE.symbol, "3")
        self.assertEqual(pkrcomponents.components.cards.rank.Rank.FOUR.symbol, "4")
        self.assertEqual(pkrcomponents.components.cards.rank.Rank.FIVE.symbol, "5")
        self.assertEqual(pkrcomponents.components.cards.rank.Rank.SIX.symbol, "6")
        self.assertEqual(pkrcomponents.components.cards.rank.Rank.SEVEN.symbol, "7")
        self.assertEqual(pkrcomponents.components.cards.rank.Rank.EIGHT.symbol, "8")
        self.assertEqual(pkrcomponents.components.cards.rank.Rank.NINE.symbol, "9")
        self.assertEqual(pkrcomponents.components.cards.rank.Rank.TEN.symbol, "T")
        self.assertEqual(pkrcomponents.components.cards.rank.Rank.JACK.symbol, "J")
        self.assertEqual(pkrcomponents.components.cards.rank.Rank.QUEEN.symbol, "Q")
        self.assertEqual(pkrcomponents.components.cards.rank.Rank.KING.symbol, "K")

    def test_ranks_contains(self):
        self.assertIn(pkrcomponents.components.cards.rank.Rank.ACE, self.all_ranks)
        self.assertIn(pkrcomponents.components.cards.rank.Rank.DEUCE, self.all_ranks)
        self.assertIn(pkrcomponents.components.cards.rank.Rank.THREE, self.all_ranks)
        self.assertIn(pkrcomponents.components.cards.rank.Rank.FOUR, self.all_ranks)
        self.assertIn(pkrcomponents.components.cards.rank.Rank.FIVE, self.all_ranks)
        self.assertIn(pkrcomponents.components.cards.rank.Rank.SIX, self.all_ranks)
        self.assertIn(pkrcomponents.components.cards.rank.Rank.SEVEN, self.all_ranks)
        self.assertIn(pkrcomponents.components.cards.rank.Rank.EIGHT, self.all_ranks)
        self.assertIn(pkrcomponents.components.cards.rank.Rank.NINE, self.all_ranks)
        self.assertIn(pkrcomponents.components.cards.rank.Rank.TEN, self.all_ranks)
        self.assertIn(pkrcomponents.components.cards.rank.Rank.JACK, self.all_ranks)
        self.assertIn(pkrcomponents.components.cards.rank.Rank.QUEEN, self.all_ranks)
        self.assertIn(pkrcomponents.components.cards.rank.Rank.KING, self.all_ranks)

    def test_rank_order(self):
        self.assertGreater(pkrcomponents.components.cards.rank.Rank("5"), pkrcomponents.components.cards.rank.Rank("2"))
        self.assertLess(pkrcomponents.components.cards.rank.Rank("3"), pkrcomponents.components.cards.rank.Rank("A"))
        self.assertLess(pkrcomponents.components.cards.rank.Rank("K"), pkrcomponents.components.cards.rank.Rank("A"))
        self.assertLess(pkrcomponents.components.cards.rank.Rank("K"), pkrcomponents.components.cards.rank.Rank(1))

    def test_rank_conversion(self):
        self.assertEqual(pkrcomponents.components.cards.rank.Rank(1), pkrcomponents.components.cards.rank.Rank("A"))
        self.assertEqual(pkrcomponents.components.cards.rank.Rank("T"), pkrcomponents.components.cards.rank.Rank.TEN)
        self.assertEqual(pkrcomponents.components.cards.rank.Rank(10), pkrcomponents.components.cards.rank.Rank("T"))

    def test_rank_equality(self):
        self.assertEqual(pkrcomponents.components.cards.rank.Rank.NINE, pkrcomponents.components.cards.rank.Rank.NINE)
        self.assertNotEqual(pkrcomponents.components.cards.rank.Rank(10), pkrcomponents.components.cards.rank.Rank(1))

    def test_rank_difference(self):
        self.assertEqual(
            pkrcomponents.components.cards.rank.Rank.difference(pkrcomponents.components.cards.rank.Rank.NINE, pkrcomponents.components.cards.rank.Rank.SEVEN), 2)

    def test_rank_difference_operator(self):
        self.assertEqual(pkrcomponents.components.cards.rank.Rank.NINE - pkrcomponents.components.cards.rank.Rank.SEVEN, 2)
        self.assertEqual(pkrcomponents.components.cards.rank.Rank.ACE - pkrcomponents.components.cards.rank.Rank.SEVEN, 6)
        self.assertEqual(pkrcomponents.components.cards.rank.Rank.ACE - pkrcomponents.components.cards.rank.Rank.EIGHT, 6)
        self.assertEqual(pkrcomponents.components.cards.rank.Rank.KING - pkrcomponents.components.cards.rank.Rank.THREE, 10)
        self.assertEqual(pkrcomponents.components.cards.rank.Rank.ACE - pkrcomponents.components.cards.rank.Rank.THREE, 2)
        self.assertEqual(pkrcomponents.components.cards.rank.Rank.FIVE - pkrcomponents.components.cards.rank.Rank.JACK, 6)

    def test_rank_order_operator(self):
        self.assertTrue(pkrcomponents.components.cards.rank.Rank.NINE > pkrcomponents.components.cards.rank.Rank.SIX)
        self.assertFalse(pkrcomponents.components.cards.rank.Rank.NINE > pkrcomponents.components.cards.rank.Rank.KING)

    def test_face_ranks(self):
        self.assertNotIn(pkrcomponents.components.cards.rank.Rank.TEN, pkrcomponents.components.cards.rank.FACE_RANKS)
        self.assertIn(pkrcomponents.components.cards.rank.Rank.KING, pkrcomponents.components.cards.rank.FACE_RANKS)
        self.assertIn(pkrcomponents.components.cards.rank.Rank.QUEEN, pkrcomponents.components.cards.rank.FACE_RANKS)
        self.assertIn(pkrcomponents.components.cards.rank.Rank.JACK, pkrcomponents.components.cards.rank.FACE_RANKS)

    def test_broadway_ranks(self):
        self.assertIn(pkrcomponents.components.cards.rank.Rank.TEN, pkrcomponents.components.cards.rank.BROADWAY_RANKS)
        self.assertIn(pkrcomponents.components.cards.rank.Rank.KING, pkrcomponents.components.cards.rank.BROADWAY_RANKS)
        self.assertIn(pkrcomponents.components.cards.rank.Rank.QUEEN, pkrcomponents.components.cards.rank.BROADWAY_RANKS)
        self.assertIn(pkrcomponents.components.cards.rank.Rank.JACK, pkrcomponents.components.cards.rank.BROADWAY_RANKS)
        self.assertIn(pkrcomponents.components.cards.rank.Rank.ACE, pkrcomponents.components.cards.rank.BROADWAY_RANKS)

    def test_is_broadway(self):
        self.assertTrue(pkrcomponents.components.cards.rank.Rank.ACE.is_broadway)
        self.assertTrue(pkrcomponents.components.cards.rank.Rank.KING.is_broadway)
        self.assertTrue(pkrcomponents.components.cards.rank.Rank.QUEEN.is_broadway)
        self.assertTrue(pkrcomponents.components.cards.rank.Rank.JACK.is_broadway)
        self.assertTrue(pkrcomponents.components.cards.rank.Rank.TEN.is_broadway)
        self.assertFalse(pkrcomponents.components.cards.rank.Rank.NINE.is_broadway)
        self.assertFalse(pkrcomponents.components.cards.rank.Rank.EIGHT.is_broadway)
        self.assertFalse(pkrcomponents.components.cards.rank.Rank.SEVEN.is_broadway)
        self.assertFalse(pkrcomponents.components.cards.rank.Rank.SIX.is_broadway)
        self.assertFalse(pkrcomponents.components.cards.rank.Rank.FIVE.is_broadway)
        self.assertFalse(pkrcomponents.components.cards.rank.Rank.FOUR.is_broadway)
        self.assertFalse(pkrcomponents.components.cards.rank.Rank.THREE.is_broadway)
        self.assertFalse(pkrcomponents.components.cards.rank.Rank.DEUCE.is_broadway)

    def test_is_face(self):
        self.assertTrue(pkrcomponents.components.cards.rank.Rank.KING.is_face)
        self.assertTrue(pkrcomponents.components.cards.rank.Rank.QUEEN.is_face)
        self.assertTrue(pkrcomponents.components.cards.rank.Rank.JACK.is_face)
        self.assertFalse(pkrcomponents.components.cards.rank.Rank.ACE.is_face)
        self.assertFalse(pkrcomponents.components.cards.rank.Rank.TEN.is_face)
        self.assertFalse(pkrcomponents.components.cards.rank.Rank.NINE.is_face)
        self.assertFalse(pkrcomponents.components.cards.rank.Rank.EIGHT.is_face)
        self.assertFalse(pkrcomponents.components.cards.rank.Rank.SEVEN.is_face)
        self.assertFalse(pkrcomponents.components.cards.rank.Rank.SIX.is_face)
        self.assertFalse(pkrcomponents.components.cards.rank.Rank.FIVE.is_face)
        self.assertFalse(pkrcomponents.components.cards.rank.Rank.FOUR.is_face)
        self.assertFalse(pkrcomponents.components.cards.rank.Rank.THREE.is_face)
        self.assertFalse(pkrcomponents.components.cards.rank.Rank.DEUCE.is_face)

    def test_short_name(self):
        self.assertEqual(pkrcomponents.components.cards.rank.Rank.ACE.short_name, "A")
        self.assertEqual(pkrcomponents.components.cards.rank.Rank.DEUCE.short_name, "2")
        self.assertEqual(pkrcomponents.components.cards.rank.Rank.THREE.short_name, "3")
        self.assertEqual(pkrcomponents.components.cards.rank.Rank.FOUR.short_name, "4")
        self.assertEqual(pkrcomponents.components.cards.rank.Rank.FIVE.short_name, "5")
        self.assertEqual(pkrcomponents.components.cards.rank.Rank.SIX.short_name, "6")
        self.assertEqual(pkrcomponents.components.cards.rank.Rank.SEVEN.short_name, "7")
        self.assertEqual(pkrcomponents.components.cards.rank.Rank.EIGHT.short_name, "8")
        self.assertEqual(pkrcomponents.components.cards.rank.Rank.NINE.short_name, "9")
        self.assertEqual(pkrcomponents.components.cards.rank.Rank.TEN.short_name, "T")
        self.assertEqual(pkrcomponents.components.cards.rank.Rank.JACK.short_name, "J")
        self.assertEqual(pkrcomponents.components.cards.rank.Rank.QUEEN.short_name, "Q")
        self.assertEqual(pkrcomponents.components.cards.rank.Rank.KING.short_name, "K")

    def test_str(self):
        self.assertEqual(str(pkrcomponents.components.cards.rank.Rank.ACE), "A")
        self.assertEqual(str(pkrcomponents.components.cards.rank.Rank.DEUCE), "2")
        self.assertEqual(str(pkrcomponents.components.cards.rank.Rank.THREE), "3")
        self.assertEqual(str(pkrcomponents.components.cards.rank.Rank.FOUR), "4")
        self.assertEqual(str(pkrcomponents.components.cards.rank.Rank.FIVE), "5")
        self.assertEqual(str(pkrcomponents.components.cards.rank.Rank.SIX), "6")
        self.assertEqual(str(pkrcomponents.components.cards.rank.Rank.SEVEN), "7")
        self.assertEqual(str(pkrcomponents.components.cards.rank.Rank.EIGHT), "8")
        self.assertEqual(str(pkrcomponents.components.cards.rank.Rank.NINE), "9")
        self.assertEqual(str(pkrcomponents.components.cards.rank.Rank.TEN), "T")
        self.assertEqual(str(pkrcomponents.components.cards.rank.Rank.JACK), "J")
        self.assertEqual(str(pkrcomponents.components.cards.rank.Rank.QUEEN), "Q")
        self.assertEqual(str(pkrcomponents.components.cards.rank.Rank.KING), "K")


if __name__ == '__main__':
    unittest.main()
