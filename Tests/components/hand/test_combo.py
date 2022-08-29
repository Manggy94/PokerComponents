import unittest
import components.hand as hand


class MyComboTestCase(unittest.TestCase):

    def test_new_combo(self):
        combo = hand.Combo("AsAd")
        self.assertIsInstance(combo, hand.Combo)
        self.assertIsInstance(hand.Combo(combo), hand.Combo)
        self.assertRaises(ValueError, lambda: hand.Combo("Asd"))
        self.assertRaises(ValueError, lambda: hand.Combo("AsAs"))

    def test_from_cards(self):
        c1 = hand.Card("As")
        c2 = hand.Card("Kh")
        self.assertIsInstance(hand.Combo.from_cards(c1, c2), hand.Combo)
        self.assertRaises(ValueError, lambda: hand.Combo.from_cards(c1, c1))
        self.assertRaises(ValueError, lambda: hand.Combo.from_cards(c1, "As"))

    def test_str(self):
        c1 = hand.Combo("KsAd")
        c2 = hand.Combo("KsKd")
        c3 = hand.Combo("KdKs")
        self.assertEqual(f"{c1}", "AdKs")
        self.assertEqual(f"{c2}", "KsKd")
        self.assertEqual(f"{c3}", "KsKd")

    def test_eq(self):
        c4 = hand.Combo("AsJs")
        c5 = hand.Combo("JsAs")
        c6 = hand.Combo("AsAh")
        c7 = hand.Combo("AhAs")
        self.assertEqual(c4, c5)
        self.assertTrue(c4 == c5)
        self.assertNotEqual(c4, c6)
        self.assertTrue(c4 != c6)
        self.assertFalse(c6 != c7)

    def test_lt(self):
        c1 = hand.Combo("KsAd")
        c2 = hand.Combo("KsKd")
        c3 = hand.Combo("KdKs")
        c4 = hand.Combo("AsJs")
        c5 = hand.Combo("JdAs")
        self.assertTrue(c1 < c2)
        self.assertFalse(c3 < c2)
        self.assertTrue(c4 < c1)
        self.assertTrue(c1 < c2)
        self.assertTrue(c5 < c4)

    def test_to_hand(self):
        c1 = hand.Combo("AsJs")
        c2 = hand.Combo("KsKd")
        c3 = hand.Combo("JdAs")
        self.assertIsInstance(c1.to_hand(), hand.Hand)
        self.assertEqual(c1.to_hand(), hand.Hand("AJs"))
        self.assertEqual(c2.to_hand(), hand.Hand("KK"))
        self.assertEqual(c3.to_hand(), hand.Hand("AJo"))

    def test_is_suited_connector(self):
        self.assertTrue(hand.Combo("AsKs").is_suited_connector)
        self.assertTrue(hand.Combo("5s6s").is_suited_connector)
        self.assertFalse(hand.Combo("ThTs").is_suited_connector)
        self.assertFalse(hand.Combo("JsTd").is_suited_connector)

    def test_is_suited(self):
        self.assertTrue(hand.Combo("AsKs").is_suited)
        self.assertTrue(hand.Combo("5s6s").is_suited)
        self.assertFalse(hand.Combo("TsTd").is_suited)
        self.assertFalse(hand.Combo("JsTd").is_suited)

    def test_is_connector(self):
        self.assertTrue(hand.Combo("AsKs").is_connector)
        self.assertTrue(hand.Combo("5s6s").is_connector)
        self.assertFalse(hand.Combo("TsTd").is_connector)
        self.assertFalse(hand.Combo("Js9d").is_connector)

    def test_is_offsuit(self):
        self.assertFalse(hand.Combo("AsKs").is_offsuit)
        self.assertFalse(hand.Combo("5s6s").is_offsuit)
        self.assertFalse(hand.Combo("ThTd").is_offsuit)
        self.assertTrue(hand.Combo("JsTd").is_offsuit)

    def test_is_one_gapper(self):
        self.assertTrue(hand.Combo("AsQs").is_one_gapper)
        self.assertTrue(hand.Combo("5s7s").is_one_gapper)
        self.assertFalse(hand.Combo("TsTd").is_one_gapper)
        self.assertFalse(hand.Combo("JsTd").is_one_gapper)

    def test_is_two_gapper(self):
        self.assertTrue(hand.Combo("AdJs").is_two_gapper)
        self.assertTrue(hand.Combo("5d8s").is_two_gapper)
        self.assertFalse(hand.Combo("TdTs").is_two_gapper)
        self.assertFalse(hand.Combo("JsTs").is_two_gapper)

    def test_rank_difference(self):
        self.assertEqual(hand.Combo("AsQs").rank_difference, 2)
        self.assertEqual(hand.Combo("As6s").rank_difference, 5)
        self.assertEqual(hand.Combo("5sKs").rank_difference, 8)
        self.assertEqual(hand.Combo("TsTd").rank_difference, 0)
        self.assertEqual(hand.Combo("JsTd").rank_difference, 1)

    def test_is_broadway(self):
        self.assertTrue(hand.Combo("AsJs").is_broadway)
        self.assertFalse(hand.Combo("5s8s").is_broadway)
        self.assertTrue(hand.Combo("TsTd").is_broadway)
        self.assertTrue(hand.Combo("JsTd").is_broadway)

    def test_is_pair(self):
        self.assertFalse(hand.Combo("AsJs").is_pair)
        self.assertFalse(hand.Combo("5s8s").is_pair)
        self.assertTrue(hand.Combo("TsTd").is_pair)
        self.assertFalse(hand.Combo("JsTd").is_pair)


if __name__ == '__main__':
    unittest.main()