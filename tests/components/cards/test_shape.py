import unittest
from pkrcomponents.components.cards import Shape


class MyShapeTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.all_shapes = list(Shape)

    def test_shapes_length(self):
        self.assertEqual(len(self.all_shapes), 3)

    def test_shapes_contains(self):
        self.assertIn(Shape(""), self.all_shapes)
        self.assertIn(Shape("s"), self.all_shapes)
        self.assertIn(Shape("o"), self.all_shapes)

    def test_shape_values(self):
        self.assertEqual(Shape.PAIR, Shape(""))
        self.assertEqual(Shape.OFFSUIT, Shape("o"))
        self.assertEqual(Shape.SUITED, Shape("s"))
        self.assertNotEqual(Shape.PAIR, Shape("s"))

    def test_name(self):
        self.assertEqual(Shape.PAIR.name, "PAIR")
        self.assertEqual(Shape.OFFSUIT.name, "OFFSUIT")
        self.assertEqual(Shape.SUITED.name, "SUITED")

    def test_symbol(self):
        self.assertEqual(Shape.PAIR.symbol, "")
        self.assertEqual(Shape.OFFSUIT.symbol, "o")
        self.assertEqual(Shape.SUITED.symbol, "s")

    def test_adjective(self):
        self.assertEqual(Shape.PAIR.adjective, "paired")
        self.assertEqual(Shape.OFFSUIT.adjective, "offsuit")
        self.assertEqual(Shape.SUITED.adjective, "suited")


if __name__ == '__main__':
    unittest.main()
