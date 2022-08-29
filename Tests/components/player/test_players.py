import unittest
import components.player as player


class MyPlayersTestCase(unittest.TestCase):

    def setUp(self):
        self.p1 = player.Player()
        self.p2 = player.Player()
        self.p3 = player.Player()
        self.p4 = player.Player()
        self.players = player.Players()

    def test_new_players(self):
        players = player.Players()
        self.assertIsInstance(players, player.Players)
        self.assertIsInstance(players.pl_list, list)
        self.assertIsInstance(players.positions, dict)
        self.assertIsInstance(players.name_dict, dict)
        self.assertIsInstance(players.seat_dict, dict)

    def test_append(self):
        self.assertRaises(ValueError, lambda: self.players.append("Toto"))
        self.players.append(self.p1)
        self.assertEqual(self.players.pl_list[0], self.p1)
        self.assertEqual(self.players.name_dict["Villain"], self.p1)
        self.assertEqual(self.players.seat_dict[0], self.p1)




if __name__ == '__main__':
    unittest.main()
