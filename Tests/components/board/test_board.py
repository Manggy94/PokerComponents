import unittest

import pandas as pd
from components import hand
from components import board
from components import card


class MyBoardTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.board = board.Board()
        self.board2 = board.Board(("As", "Ad", "Tc", "Td", card.Card("Ah")))

    def test_new_board(self):
        new_board = board.Board()
        self.assertIsInstance(new_board, board.Board)
        self.assertIsInstance(board, pd.Series)
        new_board = board.Board(["As", "Ad", "Tc"])
        self.assertIsInstance(new_board, board.Board)
        self.assertRaises(ValueError, lambda: board.Board(["As", "As", "Tc"]))
        self.assertRaises(ValueError, lambda: board.Board(["As", "Ad", "Tc", "Td", card.Card("Ah"), "Js"]))
        new_board = board.Board(("As", "Ad", "Tc", "Td", card.Card("Ah")))
        self.assertEqual(new_board["flop_1"], "As")
        self.assertEqual(new_board["flop_2"], "Ad")
        self.assertEqual(new_board["flop_3"], "Tc")
        self.assertEqual(new_board["turn"], "Td")
        self.assertEqual(new_board["river"], "Ah")

    def test_len(self):
        self.assertIsInstance(len(self.board), int)
        self.assertEqual(len(self.board), 0)
        self.board["flop_2"] = "As"
        self.board["flop_1"] = "Ad"
        self.assertEqual(len(self.board), 2)

    def test_add(self):
        self.assertRaises(ValueError, lambda: self.board.add("AA"))
        self.board.add("As")
        self.assertEqual(self.board["flop_1"], "As")
        self.board.add("Qs")
        self.assertNotEqual(self.board["flop_2"], "As")
        self.assertEqual(self.board["flop_2"], "Qs")
        self.assertRaises(ValueError, lambda: self.board.add("Qs"))

    def test_indexing(self):
        self.assertEqual(len(self.board2), 5)
        self.assertEqual(len(self.board2[:3]), 3)

    def test_flop_combination(self):
        self.assertEqual(len(self.board2.flop_combinations), 3)
        self.assertIsInstance(self.board2.flop_combinations[0], hand.Combo)
        self.assertEqual(self.board2.flop_combinations, [hand.Combo("AsAd"), hand.Combo("AsTc"), hand.Combo("AdTc")])




if __name__ == '__main__':
    unittest.main()
