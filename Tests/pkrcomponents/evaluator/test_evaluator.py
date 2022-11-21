import unittest
import pkrcomponents.evaluator as evaluator
from pkrcomponents.lookup_table import LookupTable


class MyEvaluatorTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.ev = evaluator.Evaluator()

    def test_new(self):
        ev = evaluator.Evaluator()
        self.assertIsInstance(ev, evaluator.Evaluator)
        self.assertIsInstance(evaluator.LOOKUP_TABLE, LookupTable)

    def test_eval(self):
        self.assertIsInstance(self.ev._five(["As", "Ks", "Ts", "Js", "Qs"]), int)
        self.assertIsInstance(self.ev.evaluate(board=["As", "Ks", "Ts"], cards=["Js", "Qs"]), int)
        self.assertEqual(self.ev._five(["As", "Kd", "Ts", "Js", "Qs"]), 1600)
        self.assertEqual(self.ev.evaluate(board=["As", "Kd", "Ts", "Js", "Qs"], cards=["9s", "8h"]), 487)
        self.assertEqual(self.ev.evaluate(board=["As", "Kd", "Ts", "Js", "Qs"], cards=["9s", "8s"]), 3)
        self.assertEqual(self.ev.evaluate(board=["As", "2c", "Ts", "Js", "Qs"], cards=["2h", "5h"]), 5976)
        self.assertIsInstance(evaluator.Evaluator.get_rank_class(487), int)
        self.assertEqual(evaluator.Evaluator.get_rank_class(487), 4)
        self.assertEqual(evaluator.Evaluator.get_rank_class(11), 2)
        self.assertIsInstance(evaluator.Evaluator.score_to_string(487), str)
        self.assertEqual(evaluator.Evaluator.score_to_string(487), "Flush")
        self.assertIsInstance(evaluator.Evaluator.get_five_card_rank_percentage(487), float)
        self.assertEqual(evaluator.Evaluator.get_five_card_rank_percentage(487), 1-487 / 7462)


if __name__ == '__main__':
    unittest.main()
