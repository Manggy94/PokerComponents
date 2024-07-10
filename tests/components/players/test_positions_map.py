import unittest
from pkrcomponents.components.players.positions_map import PositionsMap
from pkrcomponents.components.players.position import Position


class TestPositionsMap(unittest.TestCase):
    def test_positions_map(self):
        positions = [Position.UTG, Position.HJ, Position.CO, Position.BTN, Position.SB]
        positions_map = PositionsMap(positions)
        self.assertEqual(positions_map.cnt_players, 5)
        self.assertTrue(positions_map.has_sb)
        self.assertTrue(positions_map.has_btn)
        self.assertFalse(positions_map.has_bb)

    def test_list_generation(self):
        positions_maps = iter(PositionsMap)
        for positions_map in positions_maps:
            self.assertIsInstance(positions_map, PositionsMap)
        self.assertEqual(PositionsMap.__len__(), 32)

    def test_repr(self):
        positions_map = list(PositionsMap)[0]
        self.assertEqual(repr(positions_map), "PositionsMap('2-BTN-SB')")
