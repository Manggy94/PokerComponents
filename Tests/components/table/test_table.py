import unittest
import numpy as np
import components.table as table


class MyTableTestCase(unittest.TestCase):

    def test_new_table(self):
        tab = table.Table()
        self.assertIsInstance(tab, table.Table)
        self.assertIsInstance(tab.deck, table.Deck)
        self.assertIsInstance(tab.board, table.Board)
        self.assertIsInstance(tab._pots, list)
        self.assertIsInstance(tab.players, table.Players)
        self.assertIsInstance(tab.current_pot, table.Pot)
        self.assertEqual(tab.pot, 0)
        self.assertEqual(tab.deck.len, 52)
        self.assertEqual(tab.board.len, 0)
        self.assertEqual(len(tab._pots), 1)
        with self.assertRaises(ValueError):
            tab.max_players = 11
        tab.max_players = 9
        self.assertEqual(tab.max_players, 9)

    def test_draws(self):
        tab = table.Table()
        tab.draw_flop("As", "Ad", "Ah")
        self.assertEqual(tab.board.len, 3)
        self.assertTrue((tab.board.values[:3] == np.array(["As", "Ad", "Ah"])).all())
        self.assertRaises(ValueError, lambda: tab.draw_flop())
        self.assertRaises(ValueError, lambda: tab.draw_turn("As"))
        self.assertRaises(ValueError, lambda: tab.draw_river("Jd"))
        tab.draw_turn("Ac")
        self.assertEqual(tab.board.len, 4)
        self.assertEqual(tab.board["turn"], "Ac")
        self.assertTrue((tab.board.values[:4] == np.array(["As", "Ad", "Ah", "Ac"])).all())
        self.assertRaises(ValueError, lambda: tab.draw_flop())
        self.assertRaises(ValueError, lambda: tab.draw_turn("Jd"))
        tab.draw_river("Jd")
        self.assertEqual(tab.board.len, 5)
        self.assertEqual(tab.board["river"], "Jd")
        self.assertTrue((tab.board.values == np.array(["As", "Ad", "Ah", "Ac", "Jd"])).all())





if __name__ == '__main__':
    unittest.main()
