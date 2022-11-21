import unittest
import pkrcomponents.table_player as player
import pkrcomponents.constants as cst


class MyPlayerTestCase(unittest.TestCase):
    def setUp(self):
        self.player = player.TablePlayer("Jean", 3, 2000)
        self.toto = player.TablePlayer(name="Toto", seat=2, stack=25500)

    def test_new_player(self):
        self.assertIsInstance(self.player, player.TablePlayer)

    def test_player_name(self):
        self.assertRaises(ValueError, lambda: player.TablePlayer("This is bullshit", 3, 3000))
        self.assertGreater(len(self.player.name), 0)
        self.assertLess(len(self.player.name), 12)
        self.assertIsInstance(self.player.name, str)
        self.assertEqual(self.player.seat, 3)

    def test_player_seat(self):
        self.assertRaises(ValueError, lambda: player.TablePlayer("Tom", 4.2, 3000))
        self.assertRaises(ValueError, lambda: player.TablePlayer("Tom", 11, 3000))
        self.assertRaises(ValueError, lambda: player.TablePlayer("Tom", -1, 3000))
        self.assertIsInstance(self.player.seat, int)
        self.assertEqual(self.player.seat, 3)

    def test_player_stack(self):
        self.assertRaises(ValueError, lambda: player.TablePlayer("Tom", 4, -3000))
        self.assertIn(type(self.player.stack), [float, int])
        self.assertEqual(self.player.stack, 2000)
        self.player.stack += 0.5
        self.assertIn(type(self.player.stack), [float, int])
        self.assertEqual(self.player.stack, 2000.5)
        self.assertFalse(self.player.is_all_in)
        self.player.stack -= 1e4
        self.assertIn(type(self.player.stack), [float, int])
        self.assertEqual(self.player.stack, 0)
        self.assertTrue(self.player.is_all_in)

    def test_player_combo(self):
        with self.assertRaises(ValueError):
            self.player.combo = "Hey"
        self.assertFalse(self.player.has_combo)
        self.player.shows("AsAd")
        self.assertIsInstance(self.player.combo, player.Combo)
        self.assertEqual(self.player.combo, player.Combo("AsAd"))
        self.player.combo = player.Combo("JdAh")
        self.assertIsInstance(self.player.combo, player.Combo)
        self.assertEqual(self.player.combo, player.Combo("AhJd"))
        self.assertTrue(self.player.has_combo)

    def test_is_hero(self):
        self.assertFalse(self.player.is_hero)
        self.player.is_hero = True
        self.assertTrue(self.player.is_hero)

    def test_position(self):
        self.assertIsNone(self.player.position)
        self.player.position = cst.Position.make_random()
        self.assertIsInstance(self.player.position, cst.Position)
        with self.assertRaises(ValueError):
            self.player.position = "ABC"
        self.player.position = "BB"
        self.assertEqual(self.player.position, cst.Position.BB)

    def test_in_game(self):
        self.assertFalse(self.player.folded)
        self.assertFalse(self.player.played)
        self.player.do_fold()
        self.assertTrue(self.player.folded)
        self.assertTrue(self.player.played)

    def test_sit_and_play_at_table(self):
        tab = player.Table()
        self.toto.sit(tab)
        self.assertFalse(self.toto.played)
        self.assertFalse(self.toto.folded)
        self.player.sit(tab)
        self.assertTrue(self.player.can_play)
        self.assertEqual(self.toto.init_stack, 25500)
        self.assertEqual(tab.players.seat_dict[2], self.toto)
        self.assertEqual(tab.players.name_dict["Toto"], self.toto)
        self.assertEqual(tab.players.pl_list[0], self.toto)
        self.toto.init_stack = 22000
        self.assertEqual(self.toto.init_stack, 22000)
        self.assertEqual(self.toto.stack, 22000)
        self.assertEqual(self.toto.max_bet(1000), 1000)
        self.assertEqual(self.toto.max_bet(100000), 22000)
        self.toto.distribute("AsAd")
        self.assertRaises(ValueError, lambda: self.player.distribute("AsKs"))
        self.toto.sit_out()
        self.assertFalse(hasattr(self.toto, "_table"))
        self.assertRaises(KeyError, lambda: tab.players.name_dict["Toto"])


if __name__ == '__main__':
    unittest.main()
