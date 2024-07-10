
import unittest
from pkrcomponents.components.actions.action import Action
from pkrcomponents.components.actions.action_move import ActionMove
from pkrcomponents.components.players.table_player import TablePlayer


class ActionTest(unittest.TestCase):

    def setUp(self) -> None:
        self.p1 = TablePlayer()

    def test_new_action(self):
        self.assertIsInstance(Action(self.p1), Action)  # add assertion here

    def test_action_player(self):
        player = TablePlayer(name="Manggy", seat=4, stack=39000)
        p2 = TablePlayer(name="Claude", seat=1, stack=3900)
        action = Action(player=player)
        self.assertIsInstance(action.player, TablePlayer)
        self.assertEqual(action.player.name, "Manggy")
        self.assertEqual(action.player.stack, 39000)
        action.player = p2
        self.assertIsInstance(action.player, TablePlayer)
        self.assertEqual(action.player.name, "Claude")
        self.assertEqual(action.player.stack, 3900)
        with self.assertRaises(TypeError):
            action.player = "abc"

    def test_action_move(self):
        action = Action(player=self.p1, move=ActionMove("raise"))
        self.assertIsInstance(action.move, ActionMove)
        self.assertEqual(action.move, ActionMove.RAISE)
        self.assertEqual(action.move.symbol, "R")
        act2 = Action(player=self.p1, move=ActionMove("folds"))
        self.assertIsInstance(act2.move, ActionMove)
        self.assertNotEqual(act2.move, ActionMove.RAISE)
        self.assertEqual(act2.move, ActionMove.FOLD)

    def test_action_value(self):
        with self.assertRaises(ValueError):
            Action(player=self.p1, value=-20)
        act2 = Action(player=self.p1, value=150)
        self.assertIsInstance(act2.value, (float, int))
        self.assertNotEqual(act2.value, 200)
        self.assertEqual(act2.value, 150)

    def test_action_str(self):
        action = Action(player=self.p1, move=ActionMove("call"), value=33.000)
        self.assertIsInstance(f"{action}", str)
        self.assertEqual(f"{action}", "Villain does a CALL for 33.0")


if __name__ == '__main__':
    unittest.main()
