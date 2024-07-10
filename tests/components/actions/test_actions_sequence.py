import unittest

from pkrcomponents.components.actions.action import Action
from pkrcomponents.components.actions.action_move import ActionMove
from pkrcomponents.components.actions.actions_sequence import ActionsSequence
from pkrcomponents.components.players.table_player import TablePlayer


class TestActionsSequence(unittest.TestCase):
    def setUp(self):
        self.player = TablePlayer("Player1")
        self.action1 = Action(self.player, ActionMove.CALL, 10)
        self.action2 = Action(self.player, ActionMove.CHECK)
        self.action3 = Action(self.player, ActionMove.FOLD)
        self.actions_sequence = ActionsSequence([self.action2, self.action1, self.action3])

    def test_symbol(self):
        self.assertEqual(self.actions_sequence.symbol, "XCF")

    def test_name(self):
        self.assertEqual(self.actions_sequence.name, "CHECK-CALL-FOLD")


