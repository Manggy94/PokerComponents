
import unittest
from pkrcomponents.components.actions.action_move import ActionMove


class ActionMoveTest(unittest.TestCase):

    def test_is_call_move(self):
        self.assertFalse(ActionMove.FOLD.is_call_move)
        self.assertTrue(ActionMove.CHECK.is_call_move)
        self.assertTrue(ActionMove.CALL.is_call_move)
        self.assertFalse(ActionMove.RAISE.is_call_move)
        self.assertFalse(ActionMove.BET.is_call_move)

    def test_is_bet_move(self):
        self.assertFalse(ActionMove.FOLD.is_bet_move)
        self.assertFalse(ActionMove.CHECK.is_bet_move)
        self.assertFalse(ActionMove.CALL.is_bet_move)
        self.assertTrue(ActionMove.RAISE.is_bet_move)
        self.assertTrue(ActionMove.BET.is_bet_move)

    def test_is_vpip_move(self):
        self.assertFalse(ActionMove.FOLD.is_vpip_move)
        self.assertFalse(ActionMove.CHECK.is_vpip_move)
        self.assertTrue(ActionMove.CALL.is_vpip_move)
        self.assertTrue(ActionMove.RAISE.is_vpip_move)
        self.assertTrue(ActionMove.BET.is_vpip_move)

    def test_verb(self):
        self.assertEqual(ActionMove.FOLD.verb, "folds")
        self.assertEqual(ActionMove.CHECK.verb, "checks")
        self.assertEqual(ActionMove.CALL.verb, "calls")
        self.assertEqual(ActionMove.RAISE.verb, "raises")
        self.assertEqual(ActionMove.BET.verb, "bets")

    def test_symbol(self):
        self.assertEqual(ActionMove.FOLD.symbol, "F")
        self.assertEqual(ActionMove.CHECK.symbol, "X")
        self.assertEqual(ActionMove.CALL.symbol, "C")
        self.assertEqual(ActionMove.RAISE.symbol, "R")
        self.assertEqual(ActionMove.BET.symbol, "B")

    def test_str_(self):
        self.assertEqual(str(ActionMove.FOLD), "F")
        self.assertEqual(str(ActionMove.CHECK), "X")
        self.assertEqual(str(ActionMove.CALL), "C")
        self.assertEqual(str(ActionMove.RAISE), "R")
        self.assertEqual(str(ActionMove.BET), "B")