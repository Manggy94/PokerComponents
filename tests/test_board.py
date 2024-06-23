import unittest

import pandas as pd
from pkrcomponents.cards.board import Board
from pkrcomponents.cards import card


class MyBoardTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.board = Board.from_cards()
        self.board2 = Board.from_cards(("As", "Ad", "Tc", "Td", card.Card("Ah")))
        self.board3 = Board.from_cards(("Qd", "Ad", "Jc", "Td", card.Card("Ah")))
        self.board4 = Board.from_cards(("Qd", "5d", "Td", "Tc", card.Card("Ah")))
        self.board5 = Board.from_cards(("As", "Ad", "Ah"))
        self.board6 = Board.from_cards(("Ks", "Qs", "Js"))

    def test_new_board(self):
        new_board = Board.from_cards()
        self.assertIsInstance(new_board, Board)
        self.assertIsInstance(new_board.cards, pd.Series)
        new_board = Board.from_cards(["As", "Ad", "Tc"])
        self.assertIsInstance(new_board, Board)
        with self.assertRaises(ValueError):
            Board.from_cards(["As", "As", "Tc"])
        with self.assertRaises(ValueError):
            Board.from_cards(["As", "Ad", "Tc", "Td", "Ah", "Js"])
        new_board = Board.from_cards(("As", "Ad", "Tc", "Td", card.Card("Ah")))
        self.assertEqual(new_board.cards["flop_1"], "As")
        self.assertEqual(new_board.cards["flop_2"], "Ad")
        self.assertEqual(new_board.cards["flop_3"], "Tc")
        self.assertEqual(new_board.cards["turn"], "Td")
        self.assertEqual(new_board.cards["river"], "Ah")

    def test_len(self):
        self.assertIsInstance(len(self.board), int)
        self.assertEqual(len(self.board), 0)
        self.board.add("As")
        self.board.add("Ad")
        self.assertEqual(len(self.board), 2)
        self.assertEqual(self.board.len, 2)

    def test_add(self):
        with self.assertRaises(ValueError):
            self.board.add("AA")
        self.board.add("As")
        self.assertEqual(self.board.cards["flop_1"], "As")
        self.board.add("Qs")
        self.assertNotEqual(self.board.cards["flop_2"], "As")
        self.assertEqual(self.board.cards["flop_2"], "Qs")
        with self.assertRaises(ValueError):
            self.board.add("Qs")

    def test_to_json(self):
        self.assertIsInstance(self.board.to_json(), dict)
        self.assertEqual(self.board.to_json(), {
            'flop_1': 'nan',
            'flop_2': 'nan',
            'flop_3': 'nan',
            'turn': 'nan',
            'river': 'nan'
        })
        self.assertEqual(self.board2.to_json(), {
            'flop_1': 'As',
            'flop_2': 'Ad',
            'flop_3': 'Tc',
            'turn': 'Td',
            'river': 'Ah'
        })

    def test_reset(self):
        self.board2.reset()
        self.assertEqual(len(self.board2), 0)
        self.assertEqual(self.board2.to_json(), {
            'flop_1': 'nan',
            'flop_2': 'nan',
            'flop_3': 'nan',
            'turn': 'nan',
            'river': 'nan'
        })

    def test_eq(self):
        self.assertEqual(self.board2, Board.from_cards(("As", "Ad", "Tc", "Td", card.Card("Ah"))))
        self.assertEqual(self.board2, Board.from_cards(("As","Tc", "Ad", "Td", "Ah")))
        self.assertNotEqual(self.board2, Board.from_cards(("As", "Tc", "Ad", "Ah", "Td")))
        self.assertNotEqual(self.board2, Board.from_cards(("As", "Ad", "Tc", "Td", card.Card("Ac"))))


if __name__ == '__main__':
    unittest.main()
