import unittest
import pkrcomponents.hand as hand


class MyShapeTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.all_shapes = list(hand.Shape)

    def test_shapes_length(self):
        self.assertEqual(len(self.all_shapes), 3)

    def test_shapes_contains(self):
        self.assertIn(hand.Shape(""), self.all_shapes)
        self.assertIn(hand.Shape("s"), self.all_shapes)
        self.assertIn(hand.Shape("o"), self.all_shapes)

    def test_shape_values(self):
        self.assertEqual(hand.Shape.PAIR, hand.Shape(""))
        self.assertEqual(hand.Shape.OFFSUIT, hand.Shape("o"))
        self.assertEqual(hand.Shape.SUITED, hand.Shape("s"))
        self.assertNotEqual(hand.Shape.PAIR, hand.Shape("s"))

    def test_name(self):
        self.assertEqual(hand.Shape.PAIR.name, "PAIR")
        self.assertEqual(hand.Shape.OFFSUIT.name, "OFFSUIT")
        self.assertEqual(hand.Shape.SUITED.name, "SUITED")

    def test_symbol(self):
        self.assertEqual(hand.Shape.PAIR.symbol, "")
        self.assertEqual(hand.Shape.OFFSUIT.symbol, "o")
        self.assertEqual(hand.Shape.SUITED.symbol, "s")

    def test_adjective(self):
        self.assertEqual(hand.Shape.PAIR.adjective, "paired")
        self.assertEqual(hand.Shape.OFFSUIT.adjective, "offsuit")
        self.assertEqual(hand.Shape.SUITED.adjective, "suited")


if __name__ == '__main__':
    unittest.main()
