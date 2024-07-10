import unittest
from pkrcomponents.components.players.table_player import TablePlayer
from pkrcomponents.components.players.players import Players
from pkrcomponents.components.tables.table import Table
from pkrcomponents.components.players.position import Position


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
        for player in self.list:
            player.sit(tab)
        self.assertEqual([pl.name for pl in tab.players], ['Toto', 'Tata', 'Titi', 'Tété'])
        self.assertEqual(tab.players.occupied_seats, [1, 2, 4, 6])
        tab.players.bb_seat = 2
        self.assertIsInstance(tab.players.positions_mapper, dict)
        self.assertEqual(tab.players.bb_seat, 2)
        self.assertEqual(tab.players.preflop_ordered_seats, [4, 6, 1, 2])
        self.assertEqual(tab.players.positions_mapper, {
            4: Position.CO,
            6: Position.BTN,
            1: Position.SB,
            2: Position.BB})
        self.assertEqual(tab.players.postflop_ordered_seats, [1, 2, 4, 6])
        tab.players.bb_seat = 3
        self.assertEqual(tab.players.bb_seat, 1)
        self.assertEqual(tab.players.preflop_ordered_seats, [2, 4, 6, 1])
        self.assertIsInstance(tab.players.occupied_seats, list)
        tab.players.bb_seat = 6
        self.assertEqual(tab.players.preflop_ordered_seats, [1, 2, 4, 6])
        self.assertNotIn(self.p5, tab.players)
        self.p5.sit(tab)
        self.assertIn(self.p5, tab.players)
        tab.players.bb_seat = 4
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
        table.players.bb_seat = 2

    def test_get_bb_from_button(self):
        table = Table()
        for pl in self.list:
            pl.sit(table)
        button_seat = 1
        bb_seat = table.players.get_bb_seat_from_button(button_seat)
        self.assertEqual(bb_seat, 4)
        table3 = Table()
        list3 = [self.p1, self.p2, self.p3, self.p4, self.p5]
        for pl in list3:
            pl.sit(table3)
        button_seat3 = 5
        bb_seat3 = table3.players.get_bb_seat_from_button(button_seat3)
        self.assertEqual(bb_seat3, 1)
        button_seat3 = 6
        bb_seat3 = table3.players.get_bb_seat_from_button(button_seat3)
        self.assertEqual(bb_seat3, 2)
        table2 = Table()
        list2 = [self.p1, self.p4]
        for pl in list2:
            pl.sit(table2)
        button_seat2 = 1
        bb_seat2 = table2.players.get_bb_seat_from_button(button_seat2)
        self.assertEqual(bb_seat2, 4)
        button_seat2 = 4
        bb_seat2 = table2.players.get_bb_seat_from_button(button_seat2)
        self.assertEqual(bb_seat2, 1)


if __name__ == '__main__':
    unittest.main()
