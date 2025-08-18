import unittest

from pkrcomponents.components.players import Position


class TestPosition(unittest.TestCase):
    def setUp(self):
        self.positions = [
            Position.UTG,
            Position.UTG1,
            Position.UTG2,
            Position.UTG3,
            Position.LJ,
            Position.HJ,
            Position.CO,
            Position.BTN,
            Position.SB,
            Position.BB
        ]
        self.position_names = ["UTG", "UTG1", "UTG2", "UTG3", "LJ", "HJ", "CO", "BTN","SB", "BB"]
        self.position_short_names = ["UTG", "UTG1", "UTG2", "UTG3", "LJ", "HJ", "CO", "BTN", "SB", "BB"]
        self.position_symbols = ["UTG", "UTG1", "UTG2", "UTG3", "LJ", "HJ", "CO", "BTN", "SB", "BB"]
        self.position_preflop_order = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.position_postflop_order = [3, 4, 5, 6, 7, 8, 9, 10, 1, 2]

    def test_position_name(self):
        test_dict = dict((zip(self.position_names, self.positions)))
        for name, position in test_dict.items():
            self.assertEqual(position.name, name)


    def test_position_short_name(self):
        test_dict = dict((zip(self.position_short_names, self.positions)))
        for short_name, position in test_dict.items():
            self.assertEqual(position.short_name, short_name)


    def test_position_symbol(self):
        test_dict = dict((zip(self.position_symbols, self.positions)))
        for symbol, position in test_dict.items():
            self.assertEqual(position.symbol, symbol)


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
        """Test preflop order of positions."""
        test_dict = dict((zip(self.position_preflop_order, self.positions)))
        for order, position in test_dict.items():
            self.assertEqual(position.preflop_order, order)


    def test_position_postflop_order(self):
        """Test postflop order of positions."""
        test_dict = dict((zip(self.position_postflop_order, self.positions)))
        for order, position in test_dict.items():
            self.assertEqual(position.postflop_order, order)
