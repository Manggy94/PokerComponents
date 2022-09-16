import unittest
import components.action as action


class MyActionTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.p1 = action.Player()

    def test_new_action(self):
        self.assertIsInstance(action.Action(self.p1), action.Action)  # add assertion here

    def test_action_player(self):
        player = action.Player(name="Manggy", seat=4, stack=39000)
        act = action.Action(player=player)
        self.assertIsInstance(act.player, action.Player)
        self.assertEqual(act.player.name, "Manggy")
        self.assertEqual(act.player.stack, 39000)

    def test_action_move(self):
        act = action.Action(player=self.p1, move="raise")
        self.assertIsInstance(act.move, action.cst.Action)
        self.assertEqual(act.move, action.cst.Action.RAISE)
        act2 = action.Action(player=self.p1, move=action.cst.Action("folds"))
        self.assertIsInstance(act2.move, action.cst.Action)
        self.assertNotEqual(act2.move, action.cst.Action.RAISE)
        self.assertEqual(act2.move, action.cst.Action.FOLD)

    def test_action_value(self):
        act = action.Action(player=self.p1, value=-20)
        self.assertIsInstance(act.value, float)
        self.assertEqual(act.value, 0)
        act2 = action.Action(player=self.p1, value=150)
        self.assertIsInstance(act2.value, float)
        self.assertNotEqual(act2.value, 200)
        self.assertEqual(act2.value, 150)

    def test_action_str(self):
        act = action.Action(player=self.p1, move="call", value=33.000)
        self.assertIsInstance(f"{act}", str)
        self.assertEqual(f"{act}", "Villain CALL for 33.0")


if __name__ == '__main__':
    unittest.main()
