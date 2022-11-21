import unittest
import pkrcomponents.hand as hand


class MyHandTestCase(unittest.TestCase):

    def test_new_hand(self):
        hd = hand.Hand("AKs")
        self.assertIsInstance(hd, hand.Hand)
        self.assertIsInstance(hd.shape, hand.Shape)
        self.assertRaises(ValueError, lambda: hand.Hand("AJt"))
        self.assertRaises(ValueError, lambda: hand.Hand("AAs"))
        self.assertRaises(ValueError, lambda: hand.Hand("AT"))
        self.assertRaises(ValueError, lambda: hand.Hand("AJTs"))
        self.assertEqual(hd.shape, hand.Shape.SUITED)
        self.assertIsInstance(hand.Hand(hd), hand.Hand)

    def test_slots(self):
        self.assertEqual(len(hand.Hand("AJo").__slots__), 3)

    def test_hash(self):
        hd = hand.Hand("AKo")
        self.assertEqual(hd.__hash__(), hd.first.__hash__() + hd.second.__hash__() + hd.shape.__hash__())

    def test_all_hands_length(self):
        self.assertEqual(len(hand.Hand._all_hands), 169)

    def test_all_hands_shapes(self):
        for hd in hand.Hand._all_hands:
            self.assertIn(hd.shape, list(hand.Shape))

    def test_get_non_pairs(self):
        non_pairs = list(hand.Hand._get_non_pairs())
        self.assertEqual(len(non_pairs), 156)
        for hd in non_pairs:
            self.assertIn(hd.shape, (hand.Shape.SUITED, hand.Shape.OFFSUIT))

    def test_get_pairs(self):
        pairs = list(hand.Hand._get_pairs())
        self.assertEqual(len(pairs), 13)
        for hd in pairs:
            self.assertEqual(hd.shape, hand.Shape.PAIR)

    def test_set_ranks_in_order(self):
        self.assertEqual(hand.Hand("KAs"), hand.Hand("AKs"))

    def test_str(self):
        hd1 = hand.Hand("TKo")
        hd2 = hand.Hand("99")
        self.assertEqual(f"{hd1}", "KTo")
        self.assertNotEqual(f"{hd1}", "TKo")
        self.assertEqual(f"{hd2}", "99")
        self.assertNotEqual(f"{hd2}", 99)

    def test_equals(self):
        self.assertRaises(ValueError, lambda: hand.Hand("T8s") == "T8s")
        self.assertTrue(hand.Hand("8Ts") == hand.Hand("T8s"))
        self.assertFalse(hand.Hand("KJo") == hand.Hand("KJs"))

    def test_lt(self):
        self.assertRaises(ValueError, lambda: hand.Hand("T8s") < "T8s")
        self.assertLess(hand.Hand("AKo"), hand.Hand("AKs"))
        self.assertLess(hand.Hand("AJs"), hand.Hand("AKs"))
        self.assertLess(hand.Hand("AJs"), hand.Hand("AKo"))
        self.assertLess(hand.Hand("AJs"), hand.Hand("AA"))
        self.assertLess(hand.Hand("AKs"), hand.Hand("22"))
        self.assertGreater(hand.Hand("AA"), hand.Hand("AKs"))
        self.assertLess(hand.Hand("KJs"), hand.Hand("AQo"))
        self.assertLess(hand.Hand("KJs"), hand.Hand("AJs"))
        self.assertFalse(hand.Hand("AKo") < hand.Hand("AKo"))

    def test_to_combos(self):
        self.assertIsInstance(hand.Hand("AKs").to_combos(), tuple)
        self.assertIsInstance(hand.Hand("AKs").to_combos()[0], hand.Combo)
        self.assertEqual(len(hand.Hand("AKs").to_combos()), 4)
        self.assertEqual(len(hand.Hand("AKo").to_combos()), 12)
        self.assertEqual(len(hand.Hand("AA").to_combos()), 6)
        self.assertIn(hand.Combo("JsTd"), hand.Hand("JTo").to_combos())

    def test_is_suited_connector(self):
        self.assertTrue(hand.Hand("AKs").is_suited_connector)
        self.assertTrue(hand.Hand("56s").is_suited_connector)
        self.assertFalse(hand.Hand("TT").is_suited_connector)
        self.assertFalse(hand.Hand("JTo").is_suited_connector)

    def test_is_suited(self):
        self.assertTrue(hand.Hand("AKs").is_suited)
        self.assertTrue(hand.Hand("56s").is_suited)
        self.assertFalse(hand.Hand("TT").is_suited)
        self.assertFalse(hand.Hand("JTo").is_suited)

    def test_is_connector(self):
        self.assertTrue(hand.Hand("AKs").is_connector)
        self.assertTrue(hand.Hand("56s").is_connector)
        self.assertFalse(hand.Hand("TT").is_connector)
        self.assertFalse(hand.Hand("J9o").is_connector)

    def test_is_offsuit(self):
        self.assertFalse(hand.Hand("AKs").is_offsuit)
        self.assertFalse(hand.Hand("56s").is_offsuit)
        self.assertFalse(hand.Hand("TT").is_offsuit)
        self.assertTrue(hand.Hand("JTo").is_offsuit)

    def test_is_one_gapper(self):
        self.assertTrue(hand.Hand("AQs").is_one_gapper)
        self.assertTrue(hand.Hand("57s").is_one_gapper)
        self.assertFalse(hand.Hand("TT").is_one_gapper)
        self.assertFalse(hand.Hand("JTo").is_one_gapper)

    def test_is_two_gapper(self):
        self.assertTrue(hand.Hand("AJs").is_two_gapper)
        self.assertTrue(hand.Hand("58s").is_two_gapper)
        self.assertFalse(hand.Hand("TT").is_two_gapper)
        self.assertFalse(hand.Hand("JTo").is_two_gapper)

    def test_rank_difference(self):
        self.assertEqual(hand.Hand("AQs").rank_difference, 2)
        self.assertEqual(hand.Hand("A6s").rank_difference, 5)
        self.assertEqual(hand.Hand("5Ks").rank_difference, 8)
        self.assertEqual(hand.Hand("TT").rank_difference, 0)
        self.assertEqual(hand.Hand("JTo").rank_difference, 1)

    def test_is_broadway(self):
        self.assertTrue(hand.Hand("AJs").is_broadway)
        self.assertFalse(hand.Hand("58s").is_broadway)
        self.assertTrue(hand.Hand("TT").is_broadway)
        self.assertTrue(hand.Hand("JTo").is_broadway)

    def test_is_pair(self):
        self.assertFalse(hand.Hand("AJs").is_pair)
        self.assertFalse(hand.Hand("58s").is_pair)
        self.assertTrue(hand.Hand("TT").is_pair)
        self.assertFalse(hand.Hand("JTo").is_pair)

    def test_make_random(self):
        shapes = []
        while len(shapes) < 3:
            hd = hand.Hand.make_random()
            self.assertIsInstance(hd, hand.Hand)
            if hd.is_pair and hand.Shape.PAIR not in shapes:
                self.assertEqual(hd.shape, hand.Shape.PAIR)
                shapes.append(hand.Shape.PAIR)
            elif hd.is_offsuit and hand.Shape.OFFSUIT not in shapes:
                self.assertEqual(hd.shape, hand.Shape.OFFSUIT)
                shapes.append(hand.Shape.OFFSUIT)
            elif hd.is_suited and hand.Shape.SUITED not in shapes:
                self.assertEqual(hd.shape, hand.Shape.SUITED)
                shapes.append(hand.Shape.SUITED)

    def test_shape(self):
        hd = hand.Hand("AKo")
        self.assertEqual(hd.shape, hand.Shape.OFFSUIT)
        hd.shape = "s"
        self.assertEqual(hd.shape, hand.Shape.SUITED)
        hd.shape = hand.Shape("o")
        self.assertEqual(hd.shape, hand.Shape.OFFSUIT)


if __name__ == '__main__':
    unittest.main()
