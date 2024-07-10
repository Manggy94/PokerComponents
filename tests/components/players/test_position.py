import unittest

from pkrcomponents.components.players.position import Position


class TestPosition(unittest.TestCase):

    def test_position_name(self):
        self.assertEqual(Position.UTG.name, "UTG")
        self.assertEqual(Position.UTG1.name, "UTG1")
        self.assertEqual(Position.UTG2.name, "UTG2")
        self.assertEqual(Position.UTG3.name, "UTG3")
        self.assertEqual(Position.LJ.name, "LJ")
        self.assertEqual(Position.HJ.name, "HJ")
        self.assertEqual(Position.CO.name, "CO")
        self.assertEqual(Position.BTN.name, "BTN")
        self.assertEqual(Position.SB.name, "SB")
        self.assertEqual(Position.BB.name, "BB")

    def test_position_short_name(self):
        self.assertEqual(Position.UTG.short_name, "UTG")
        self.assertEqual(Position.UTG1.short_name, "UTG1")
        self.assertEqual(Position.UTG2.short_name, "UTG2")
        self.assertEqual(Position.UTG3.short_name, "UTG3")
        self.assertEqual(Position.LJ.short_name, "LJ")
        self.assertEqual(Position.HJ.short_name, "HJ")
        self.assertEqual(Position.CO.short_name, "CO")
        self.assertEqual(Position.BTN.short_name, "BTN")
        self.assertEqual(Position.SB.short_name, "SB")
        self.assertEqual(Position.BB.short_name, "BB")

    def test_position_symbol(self):
        self.assertEqual(Position.UTG.symbol, "UTG")
        self.assertEqual(Position.UTG1.symbol, "UTG1")
        self.assertEqual(Position.UTG2.symbol, "UTG2")
        self.assertEqual(Position.UTG3.symbol, "UTG3")
        self.assertEqual(Position.LJ.symbol, "LJ")
        self.assertEqual(Position.HJ.symbol, "HJ")
        self.assertEqual(Position.CO.symbol, "CO")
        self.assertEqual(Position.BTN.symbol, "BTN")
        self.assertEqual(Position.SB.symbol, "SB")
        self.assertEqual(Position.BB.symbol, "BB")

    def test_position_is_early(self):
        self.assertTrue(Position.UTG.is_early)
        self.assertTrue(Position.UTG1.is_early)
        self.assertTrue(Position.UTG2.is_early)
        self.assertTrue(Position.UTG3.is_early)
        self.assertFalse(Position.LJ.is_early)
        self.assertFalse(Position.HJ.is_early)
        self.assertFalse(Position.CO.is_early)
        self.assertFalse(Position.BTN.is_early)
        self.assertFalse(Position.SB.is_early)
        self.assertFalse(Position.BB.is_early)

    def test_position_is_middle(self):
        self.assertFalse(Position.UTG.is_middle)
        self.assertFalse(Position.UTG1.is_middle)
        self.assertFalse(Position.UTG2.is_middle)
        self.assertFalse(Position.UTG3.is_middle)
        self.assertTrue(Position.LJ.is_middle)
        self.assertTrue(Position.HJ.is_middle)
        self.assertFalse(Position.CO.is_middle)
        self.assertFalse(Position.BTN.is_middle)
        self.assertFalse(Position.SB.is_middle)
        self.assertFalse(Position.BB.is_middle)

    def test_position_is_late(self):
        self.assertFalse(Position.UTG.is_late)
        self.assertFalse(Position.UTG1.is_late)
        self.assertFalse(Position.UTG2.is_late)
        self.assertFalse(Position.UTG3.is_late)
        self.assertFalse(Position.LJ.is_late)
        self.assertFalse(Position.HJ.is_late)
        self.assertTrue(Position.CO.is_late)
        self.assertTrue(Position.BTN.is_late)
        self.assertFalse(Position.SB.is_late)
        self.assertFalse(Position.BB.is_late)

    def test_position_is_blind(self):
        self.assertFalse(Position.UTG.is_blind)
        self.assertFalse(Position.UTG1.is_blind)
        self.assertFalse(Position.UTG2.is_blind)
        self.assertFalse(Position.UTG3.is_blind)
        self.assertFalse(Position.LJ.is_blind)
        self.assertFalse(Position.HJ.is_blind)
        self.assertFalse(Position.CO.is_blind)
        self.assertFalse(Position.BTN.is_blind)
        self.assertTrue(Position.SB.is_blind)
        self.assertTrue(Position.BB.is_blind)

    def test_position_preflop_order(self):
        self.assertEqual(Position.UTG.preflop_order, 1)
        self.assertEqual(Position.UTG1.preflop_order, 2)
        self.assertEqual(Position.UTG2.preflop_order, 3)
        self.assertEqual(Position.UTG3.preflop_order, 4)
        self.assertEqual(Position.LJ.preflop_order, 5)
        self.assertEqual(Position.HJ.preflop_order, 6)
        self.assertEqual(Position.CO.preflop_order, 7)
        self.assertEqual(Position.BTN.preflop_order, 8)
        self.assertEqual(Position.SB.preflop_order, 9)
        self.assertEqual(Position.BB.preflop_order, 10)

    def test_position_postflop_order(self):
        self.assertEqual(Position.UTG.postflop_order, 3)
        self.assertEqual(Position.UTG1.postflop_order, 4)
        self.assertEqual(Position.UTG2.postflop_order, 5)
        self.assertEqual(Position.UTG3.postflop_order, 6)
        self.assertEqual(Position.LJ.postflop_order, 7)
        self.assertEqual(Position.HJ.postflop_order, 8)
        self.assertEqual(Position.CO.postflop_order, 9)
        self.assertEqual(Position.BTN.postflop_order, 10)
        self.assertEqual(Position.SB.postflop_order, 1)
        self.assertEqual(Position.BB.postflop_order, 2)