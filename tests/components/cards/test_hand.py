import unittest

from pkrcomponents.components.cards.hand import Hand
from pkrcomponents.components.cards.shape import Shape


class MyHandTestCase(unittest.TestCase):

    def test_new_hand(self):
        hand = Hand("AKs")
        self.assertIsInstance(hand, Hand)
        self.assertIsInstance(hand.shape, Shape)
        self.assertRaises(ValueError, lambda: Hand("AJt"))
        self.assertRaises(ValueError, lambda: Hand("AAs"))
        self.assertRaises(ValueError, lambda: Hand("AT"))
        self.assertRaises(ValueError, lambda: Hand("AJTs"))
        self.assertEqual(hand.shape, Shape.SUITED)
        self.assertIsInstance(Hand(hand), Hand)

    def test_slots(self):
        self.assertEqual(len(Hand("AJo").__slots__), 3)

    def test_hash(self):
        hand = Hand("AKo")
        self.assertEqual(hand.__hash__(), hand.first.__hash__() + hand.second.__hash__() + hand.shape.__hash__())

    def test_all_hands_length(self):
        self.assertEqual(len(Hand.all_hands), 169)

    def test_all_hands_shapes(self):
        for hand in Hand.all_hands:
            self.assertIn(hand.shape, list(Shape))


    def test_set_ranks_in_order(self):
        self.assertEqual(Hand("KAs"), Hand("AKs"))

    def test_str(self):
        hand1 = Hand("TKo")
        hand2 = Hand("99")
        self.assertEqual(f"{hand1}", "KTo")
        self.assertNotEqual(f"{hand1}", "TKo")
        self.assertEqual(f"{hand2}", "99")

    def test_equals(self):
        self.assertRaises(ValueError, lambda: Hand("T8s") == "T8s")
        self.assertEqual(Hand("8Ts"), Hand("T8s"))
        self.assertNotEqual(Hand("KJo"), Hand("KJs"))

    def test_lt(self):
        self.assertRaises(ValueError, lambda: Hand("T8s") < "T8s")
        self.assertLess(Hand("AKo"), Hand("AKs"))
        self.assertLess(Hand("AJs"), Hand("AKs"))
        self.assertLess(Hand("AJs"), Hand("AKo"))
        self.assertLess(Hand("AJs"), Hand("AA"))
        self.assertLess(Hand("AKs"), Hand("22"))
        self.assertGreater(Hand("AA"), Hand("AKs"))
        self.assertLess(Hand("KJs"), Hand("AQo"))
        self.assertLess(Hand("KJs"), Hand("AJs"))
        self.assertFalse(Hand("AKo") < Hand("AKo"))


    def test_is_suited_connector(self):
        self.assertTrue(Hand("AKs").is_suited_connector)
        self.assertTrue(Hand("56s").is_suited_connector)
        self.assertFalse(Hand("TT").is_suited_connector)
        self.assertFalse(Hand("JTo").is_suited_connector)

    def test_is_suited(self):
        self.assertTrue(Hand("AKs").is_suited)
        self.assertTrue(Hand("56s").is_suited)
        self.assertFalse(Hand("TT").is_suited)
        self.assertFalse(Hand("JTo").is_suited)

    def test_is_connector(self):
        self.assertTrue(Hand("AKs").is_connector)
        self.assertTrue(Hand("56s").is_connector)
        self.assertFalse(Hand("TT").is_connector)
        self.assertFalse(Hand("J9o").is_connector)

    def test_is_offsuit(self):
        self.assertFalse(Hand("AKs").is_offsuit)
        self.assertFalse(Hand("56s").is_offsuit)
        self.assertFalse(Hand("TT").is_offsuit)
        self.assertTrue(Hand("JTo").is_offsuit)

    def test_is_one_gapper(self):
        self.assertTrue(Hand("AQs").is_one_gapper)
        self.assertTrue(Hand("57s").is_one_gapper)
        self.assertFalse(Hand("TT").is_one_gapper)
        self.assertFalse(Hand("JTo").is_one_gapper)

    def test_is_two_gapper(self):
        self.assertTrue(Hand("AJs").is_two_gapper)
        self.assertTrue(Hand("58s").is_two_gapper)
        self.assertFalse(Hand("TT").is_two_gapper)
        self.assertFalse(Hand("JTo").is_two_gapper)

    def test_rank_difference(self):
        self.assertEqual(Hand("AQs").rank_difference, 2)
        self.assertEqual(Hand("A6s").rank_difference, 5)
        self.assertEqual(Hand("5Ks").rank_difference, 8)
        self.assertEqual(Hand("TT").rank_difference, 0)
        self.assertEqual(Hand("JTo").rank_difference, 1)

    def test_is_broadway(self):
        self.assertTrue(Hand("AJs").is_broadway)
        self.assertFalse(Hand("58s").is_broadway)
        self.assertTrue(Hand("TT").is_broadway)
        self.assertTrue(Hand("JTo").is_broadway)

    def test_is_pair(self):
        self.assertFalse(Hand("AJs").is_pair)
        self.assertFalse(Hand("58s").is_pair)
        self.assertTrue(Hand("TT").is_pair)
        self.assertFalse(Hand("JTo").is_pair)

    def test_make_random(self):
        shapes = []
        while len(shapes) < 3:
            hand = Hand.make_random()
            self.assertIsInstance(hand, Hand)
            if hand.is_pair and Shape.PAIR not in shapes:
                self.assertEqual(hand.shape, Shape.PAIR)
                shapes.append(Shape.PAIR)
            elif hand.is_offsuit and Shape.OFFSUIT not in shapes:
                self.assertEqual(hand.shape, Shape.OFFSUIT)
                shapes.append(Shape.OFFSUIT)
            elif hand.is_suited and Shape.SUITED not in shapes:
                self.assertEqual(hand.shape, Shape.SUITED)
                shapes.append(Shape.SUITED)

    def test_shape(self):
        hand = Hand("AKo")
        self.assertEqual(hand.shape, Shape.OFFSUIT)
        hand.shape = "s"
        self.assertEqual(hand.shape, Shape.SUITED)
        hand.shape = Shape("o")
        self.assertEqual(hand.shape, Shape.OFFSUIT)

    def test_short_name(self):
        self.assertEqual(Hand("AKs").short_name, "AKs")
        self.assertEqual(Hand("AKo").short_name, "AKo")
        self.assertEqual(Hand("TT").short_name, "TT")

    def test_symbol(self):
        self.assertEqual(Hand("AKs").symbol, "AKs")
        self.assertEqual(Hand("AKo").symbol, "AKo")
        self.assertEqual(Hand("TT").symbol, "TT")

    def test_is_face(self):
        self.assertFalse(Hand("AKs").is_face)
        self.assertFalse(Hand("56s").is_face)
        self.assertTrue(Hand("KQo").is_face)
        self.assertFalse(Hand("JTo").is_face)

    def test_non_paired_hands(self):
        non_pairs = list(Hand.get_non_paired_hands())
        self.assertEqual(len(non_pairs), 156)
        for hand in non_pairs:
            self.assertIn(hand.shape, (Shape.SUITED, Shape.OFFSUIT))

    def test_paired_hands(self):
        paired_hands = tuple(Hand.get_paired_hands())
        self.assertEqual(len(paired_hands), 13)
        for hand in paired_hands:
            self.assertEqual(hand.shape, Shape.PAIR)

    def test_offsuit_hands(self):
        offsuit_hands = tuple(Hand.get_offsuit_hands())
        self.assertEqual(len(offsuit_hands), 78)
        for hand in offsuit_hands:
            self.assertEqual(hand.shape, Shape.OFFSUIT)

    def test_suited_hands(self):
        suited_hands = tuple(Hand.get_suited_hands())
        self.assertEqual(len(suited_hands), 78)
        for hand in suited_hands:
            self.assertEqual(hand.shape, Shape.SUITED)

    def test_list_generation(self):
        hands = iter(Hand)
        for hand in hands:
            self.assertIsInstance(hand, Hand)
        self.assertEqual(Hand.__len__(), 169)


if __name__ == '__main__':
    unittest.main()
