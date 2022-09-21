import unittest
import components.table_player as player
import components.players as players


class MyPlayersTestCase(unittest.TestCase):

    def setUp(self):
        self.p1 = player.TablePlayer()
        self.p2 = player.TablePlayer()
        self.p3 = player.TablePlayer()
        self.p4 = player.TablePlayer()
        self.players = players.Players()

    def test_new_players(self):
        plrs = players.Players()
        self.assertIsInstance(plrs, players.Players)
        self.assertIsInstance(plrs.pl_list, list)
        self.assertIsInstance(plrs.positions, dict)
        self.assertIsInstance(plrs.name_dict, dict)
        self.assertIsInstance(plrs.seat_dict, dict)

    def test_append(self):
        self.assertRaises(ValueError, lambda: self.players.append("Toto"))
        self.players.append(self.p1)
        self.assertEqual(self.players.pl_list[0], self.p1)
        self.assertEqual(self.players.name_dict["Villain"], self.p1)
        self.assertEqual(self.players.seat_dict[0], self.p1)


if __name__ == '__main__':
    unittest.main()
