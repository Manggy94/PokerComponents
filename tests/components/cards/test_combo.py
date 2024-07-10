import unittest

from pkrcomponents.components.cards.combo import Combo
from pkrcomponents.components.cards.hand import Hand
from pkrcomponents.components.cards.card import Card


class MyComboTestCase(unittest.TestCase):

    def test_new_combo(self):
        combo = Combo("AsAd")
        self.assertIsInstance(combo, Combo)
        self.assertIsInstance(Combo(combo), Combo)
        self.assertRaises(ValueError, lambda: Combo("Asd"))
        self.assertRaises(ValueError, lambda: Combo("AsAs"))

    def test_from_cards(self):
        c1 = Card("As")
        c2 = Card("Kh")
        self.assertIsInstance(Combo.from_cards(c1, c2), Combo)
        self.assertRaises(ValueError, lambda: Combo.from_cards(c1, c1))
        self.assertRaises(ValueError, lambda: Combo.from_cards(c1, "Ab"))
        self.assertEqual(Combo.from_cards(c1, "Ad"), Combo("AsAd"))

    def test_from_tuple(self):
        c1 = Card("As")
        c2 = Card("Kh")
        c3 = Card("Js")
        self.assertIsInstance(Combo.from_tuple((c1, c2)), Combo)
        self.assertRaises(ValueError, lambda: Combo.from_tuple((c1, c1)))
        self.assertRaises(TypeError, lambda: Combo.from_tuple(c1, c1))
        self.assertRaises(ValueError, lambda: Combo.from_tuple([c1, c2]))
        self.assertRaises(ValueError, lambda: Combo.from_tuple((c1, "Ab")))
        self.assertRaises(ValueError, lambda: Combo.from_tuple((c1, c2, c3)))
        self.assertEqual(Combo.from_tuple((c1, "Ad")), Combo("AsAd"))

    def test_str(self):
        c1 = Combo("KsAd")
        c2 = Combo("KsKd")
        c3 = Combo("KdKs")
        self.assertEqual(f"{c1}", "AdKs")
        self.assertEqual(f"{c2}", "KsKd")
        self.assertEqual(f"{c3}", "KsKd")

    def test_hash(self):
        c1 = Combo("AsAd")
        self.assertEqual(c1.__hash__(), c1.first.__hash__() + c1.second.__hash__())

    def test_eq(self):
        c4 = Combo("AsJs")
        c5 = Combo("JsAs")
        c6 = Combo("AsAh")
        c7 = Combo("AhAs")
        self.assertRaises(ValueError, lambda: c4 == "AsJs")
        self.assertEqual(c4, c5)
        self.assertNotEqual(c4, c6)
        self.assertEqual(c6, c7)

    def test_lt(self):
        c1 = Combo("KsAd")
        c2 = Combo("KsKd")
        c3 = Combo("KdKs")
        c4 = Combo("AsJs")
        c5 = Combo("JdAs")
        c6 = Combo("AsAd")
        self.assertRaises(ValueError, lambda: c4 < "AsJs")

        self.assertTrue(c1 < c2)
        self.assertFalse(c3 < c2)
        self.assertTrue(c4 < c1)
        self.assertTrue(c1 < c2)
        self.assertTrue(c5 < c4)
        self.assertTrue(c2 < c6)
        self.assertTrue(c1 > Hand("ATo"))

    def test_set_cards_in_order(self):
        c1 = Combo("AsJd")
        self.assertEqual(c1.first, Card("As"))
        self.assertEqual(c1.second, Card("Jd"))
        c1.first, c1.second = c1.second, c1.first
        self.assertNotEqual(c1.first, Card("As"))
        self.assertNotEqual(c1.second, Card("Jd"))
        c1._set_cards_in_order(c1.first, c1.second)
        self.assertEqual(c1.first, Card("As"))
        self.assertEqual(c1.second, Card("Jd"))

    def test_to_hand(self):
        c1 = Combo("AsJs")
        c2 = Combo("KsKd")
        c3 = Combo("JdAs")
        self.assertIsInstance(c1.hand, Hand)
        self.assertEqual(c1.hand, Hand("AJs"))
        self.assertEqual(c2.hand, Hand("KK"))
        self.assertEqual(c3.hand, Hand("AJo"))

    def test_is_suited_connector(self):
        self.assertTrue(Combo("AsKs").is_suited_connector)
        self.assertTrue(Combo("5s6s").is_suited_connector)
        self.assertFalse(Combo("ThTs").is_suited_connector)
        self.assertFalse(Combo("JsTd").is_suited_connector)

    def test_is_suited(self):
        self.assertTrue(Combo("AsKs").is_suited)
        self.assertTrue(Combo("5s6s").is_suited)
        self.assertFalse(Combo("TsTd").is_suited)
        self.assertFalse(Combo("JsTd").is_suited)

    def test_is_connector(self):
        self.assertTrue(Combo("AsKs").is_connector)
        self.assertTrue(Combo("5s6s").is_connector)
        self.assertFalse(Combo("TsTd").is_connector)
        self.assertFalse(Combo("Js9d").is_connector)

    def test_is_offsuit(self):
        self.assertFalse(Combo("AsKs").is_offsuit)
        self.assertFalse(Combo("5s6s").is_offsuit)
        self.assertFalse(Combo("ThTd").is_offsuit)
        self.assertTrue(Combo("JsTd").is_offsuit)

    def test_is_one_gapper(self):
        self.assertTrue(Combo("AsQs").is_one_gapper)
        self.assertTrue(Combo("5s7s").is_one_gapper)
        self.assertFalse(Combo("TsTd").is_one_gapper)
        self.assertFalse(Combo("JsTd").is_one_gapper)

    def test_is_two_gapper(self):
        self.assertTrue(Combo("AdJs").is_two_gapper)
        self.assertTrue(Combo("5d8s").is_two_gapper)
        self.assertFalse(Combo("TdTs").is_two_gapper)
        self.assertFalse(Combo("JsTs").is_two_gapper)

    def test_rank_difference(self):
        self.assertEqual(Combo("AsQs").rank_difference, 2)
        self.assertEqual(Combo("As6s").rank_difference, 5)
        self.assertEqual(Combo("5sKs").rank_difference, 8)
        self.assertEqual(Combo("TsTd").rank_difference, 0)
        self.assertEqual(Combo("JsTd").rank_difference, 1)

    def test_is_broadway(self):
        self.assertTrue(Combo("AsJs").is_broadway)
        self.assertFalse(Combo("5s8s").is_broadway)
        self.assertTrue(Combo("TsTd").is_broadway)
        self.assertTrue(Combo("JsTd").is_broadway)

    def test_is_pair(self):
        self.assertFalse(Combo("AsJs").is_pair)
        self.assertFalse(Combo("5s8s").is_pair)
        self.assertTrue(Combo("TsTd").is_pair)
        self.assertFalse(Combo("JsTd").is_pair)

    def test_from_hand(self):
        self.assertIsInstance(Combo.from_hand(Hand("AKs")), tuple)
        self.assertIsInstance(Combo.from_hand(Hand("AKs"))[0], Combo)
        self.assertEqual(len(Combo.from_hand(Hand("AKs"))), 4)
        self.assertEqual(len(Combo.from_hand(Hand("AKo"))), 12)
        self.assertEqual(len(Combo.from_hand(Hand("AA"))), 6)
        self.assertIn(Combo("JsTd"), Combo.from_hand(Hand("JTo")))

    def test_list_generation(self):
        combos = iter(Combo)
        for combo in combos:
            self.assertIsInstance(combo, Combo)
        self.assertEqual(Combo.__len__(), 1326)


if __name__ == '__main__':
    unittest.main()
