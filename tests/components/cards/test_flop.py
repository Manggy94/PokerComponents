import unittest
from pkrcomponents.components.cards.card import Card
from pkrcomponents.components.cards.flop import Flop


class FlopTest(unittest.TestCase):

    def setUp(self):
        self.flop = Flop(Card("As"), Card("Ad"), Card("Tc"))

    def test_is_rainbow(self):
        self.assertTrue(self.flop.is_rainbow)
        flop = Flop(Card("As"), Card("Ks"), Card("Ts"))
        self.assertFalse(flop.is_rainbow)

    def test_has_flush(self):
        self.assertFalse(self.flop.has_flush_draw)
        flop = Flop(Card("As"), Card("Ks"), Card("Ts"))
        self.assertTrue(flop.has_flush_draw)

    def test_is_monotone_(self):
        self.assertFalse(self.flop.is_monotone)
        flop = Flop(Card("As"), Card("Ks"), Card("Ts"))
        self.assertTrue(flop.is_monotone)

    def test_is_triplet(self):
        self.assertFalse(self.flop.is_triplet)
        flop = Flop(Card("As"), Card("Ad"), Card("Ac"))
        self.assertTrue(flop.is_triplet)

    def test_is_paired(self):
        self.assertTrue(self.flop.is_paired)
        flop = Flop(Card("As"), Card("Ad"), Card("Kc"))
        flop2 = Flop(Card("As"), Card("Kd"), Card("Qc"))
        self.assertTrue(flop.is_paired)
        self.assertFalse(flop2.is_paired)

    def test_short_name(self):
        self.assertEqual(self.flop.short_name, "AsAdTc")
        flop = Flop(Card("As"), Card("Ks"), Card("Ts"))
        self.assertEqual(flop.short_name, "AsKsTs")

    def test_duos(self):
        self.assertEqual(len(self.flop.duos), 3)
        self.assertEqual(self.flop.duos[0], (Card("As"), Card("Ad")))
        self.assertEqual(self.flop.duos[1], (Card("As"), Card("Tc")))
        self.assertEqual(self.flop.duos[2], (Card("Ad"), Card("Tc")))

    def test_differences(self):
        self.assertEqual(len(self.flop.differences), 2)
        self.assertEqual(self.flop.differences, {0, 4})

    def test_min_distance(self):
        self.assertEqual(self.flop.min_distance, 0)
        flop = Flop(Card("As"), Card("Ks"), Card("Ts"))
        self.assertEqual(flop.min_distance, 1)

    def test_max_distance(self):
        self.assertEqual(self.flop.max_distance, 4)
        flop = Flop(Card("As"), Card("Ks"), Card("Ts"))
        self.assertEqual(flop.max_distance, 4)

    def test_has_straight_draw(self):
        self.assertFalse(self.flop.has_straight_draw)
        flop = Flop(Card("As"), Card("Ks"), Card("Ts"))
        self.assertTrue(flop.has_straight_draw)
        flop2 = Flop(Card("Ks"), Card("2s"), Card("7s"))
        self.assertFalse(flop2.has_straight_draw)

    def test_has_gutshot(self):
        self.assertTrue(self.flop.has_gutshot)
        flop = Flop(Card("As"), Card("Ks"), Card("Ts"))
        self.assertTrue(flop.has_gutshot)
        flop2 = Flop(Card("Ks"), Card("2s"), Card("7s"))
        self.assertFalse(flop2.has_gutshot)

    def test_is_sequential(self):
        self.assertFalse(self.flop.is_sequential)
        flop = Flop(Card("As"), Card("Ks"), Card("Ts"))
        self.assertFalse(flop.is_sequential)
        flop2 = Flop(Card("4s"), Card("2s"), Card("3d"))
        self.assertTrue(flop2.is_sequential)

    def test_has_straights(self):
        self.assertFalse(self.flop.has_straights)
        flop = Flop(Card("As"), Card("Ks"), Card("Ts"))
        self.assertTrue(flop.has_straights)
        flop2 = Flop(Card("4s"), Card("2s"), Card("3d"))
        self.assertTrue(flop2.has_straights)

    def test_from_string(self):
        flop = Flop.from_string("AsAdTc")
        self.assertEqual(flop, self.flop)
        flop = Flop.from_string("AsKsTs")
        self.assertEqual(flop, Flop(Card("As"), Card("Ks"), Card("Ts")))

    def test_symbol(self):
        self.assertEqual(self.flop.symbol, "A♠A♦T♣")
        flop = Flop(Card("As"), Card("Ts"), Card("Ks"))
        self.assertEqual(flop.symbol, "A♠K♠T♠")

    def test_eq(self):
        flop = Flop(Card("Ad"), Card("As"), Card("Tc"))
        self.assertEqual(flop, self.flop)
        flop = Flop(Card("As"), Card("Ks"), Card("Ts"))
        self.assertNotEqual(flop, self.flop)

    def test_repr(self):
        self.assertEqual(repr(self.flop), "Flop('AsAdTc')")

    def test_list_generation(self):
        flops = iter(Flop)
        for flop in flops:
            self.assertIsInstance(flop, Flop)
        self.assertEqual(Flop.__len__(), 22100)


