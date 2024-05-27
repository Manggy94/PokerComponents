import unittest
from pkrcomponents.table_player import TablePlayer
from pkrcomponents.players import Players
from pkrcomponents.table import Table
from pkrcomponents.constants import Position


class PlayersTest(unittest.TestCase):

    def setUp(self):
        self.p1 = TablePlayer(name="Toto", seat=1)
        self.p2 = TablePlayer(name="Tata", seat=2)
        self.p3 = TablePlayer(name="Titi", seat=6)
        self.p4 = TablePlayer(name="Tété", seat=4)
        self.p5 = TablePlayer(name="Tutu", seat=5)
        self.list = [self.p1, self.p2, self.p3, self.p4]
        self.players = Players()

    def test_new_players(self):
        players = Players()
        self.assertIsInstance(players, Players)
        self.assertIsInstance(players.pl_list, list)
        self.assertIsInstance(players.name_dict, dict)
        self.assertIsInstance(players.seat_dict, dict)

    def test_occupied_and_distribute_positions(self):
        tab = Table()
        for pl in self.list:
            pl.sit(tab)
        self.assertEqual([pl.name for pl in tab.players], ['Toto', 'Tata', 'Titi', 'Tété'])
        self.assertEqual(tab.players.occupied_seats, [1, 2, 4, 6])
        tab.players.bb = 2
        self.assertIsInstance(tab.players.positions_mapper, dict)
        self.assertEqual(tab.players.bb, 2)
        self.assertEqual(tab.players.preflop_ordered_seats, [4, 6, 1, 2])
        self.assertEqual(tab.players.positions_mapper, {
            4: Position.CO,
            6: Position.BTN,
            1: Position.SB,
            2: Position.BB})
        self.assertEqual(tab.players.postflop_ordered_seats, [1, 2, 4, 6])
        tab.players.bb = 3
        self.assertEqual(tab.players.bb, 1)
        self.assertEqual(tab.players.preflop_ordered_seats, [2, 4, 6, 1])
        self.assertIsInstance(tab.players.occupied_seats, list)
        tab.players.bb = 6
        self.assertEqual(tab.players.preflop_ordered_seats, [1, 2, 4, 6])
        self.assertNotIn(self.p5, tab.players)
        self.p5.sit(tab)
        self.assertIn(self.p5, tab.players)
        tab.players.bb = 4
        self.assertEqual(tab.players.occupied_seats, [1, 2, 4, 5, 6])
        self.assertEqual(tab.players.preflop_ordered_seats, [5, 6, 1, 2, 4])
        self.assertEqual(tab.players.positions_mapper, {
            5: Position.HJ,
            6: Position.CO,
            1: Position.BTN,
            2: Position.SB,
            4: Position.BB})
        tab.players.distribute_positions()
        self.assertEqual(tab.players.postflop_ordered_seats, [2, 4, 5, 6, 1])
        self.assertEqual(tab.players["Titi"].position, Position("cutoff"))
        self.assertEqual(tab.players[5].position, Position.HJ)
        self.assertRaises(ValueError, lambda: tab.players[0.5])

    def test_advance_bb_seat(self):
        table = Table()
        for pl in self.list:
            pl.sit(table)
        table.players.bb = 2


if __name__ == '__main__':
    unittest.main()
