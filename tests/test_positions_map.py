import unittest
from pkrcomponents.players.positions_map import PositionsMap
from pkrcomponents.players.position import Position


class TestPositionsMap(unittest.TestCase):
    def test_positions_map(self):
        positions = [Position.UTG, Position.HJ, Position.CO, Position.BTN, Position.SB]
        positions_map = PositionsMap(positions)
        self.assertEqual(positions_map.cnt_players, 5)
        self.assertTrue(positions_map.has_sb)
        self.assertTrue(positions_map.has_btn)
        self.assertFalse(positions_map.has_bb)
