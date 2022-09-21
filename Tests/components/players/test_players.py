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


if __name__ == '__main__':
    unittest.main()
