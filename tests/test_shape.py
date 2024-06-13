import unittest
import pkrcomponents.hand as hand
import pkrcomponents.shape


class MyShapeTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.all_shapes = list(pkrcomponents.shape.Shape)

    def test_shapes_length(self):
        self.assertEqual(len(self.all_shapes), 3)

    def test_shapes_contains(self):
        self.assertIn(pkrcomponents.shape.Shape(""), self.all_shapes)
        self.assertIn(pkrcomponents.shape.Shape("s"), self.all_shapes)
        self.assertIn(pkrcomponents.shape.Shape("o"), self.all_shapes)

    def test_shape_values(self):
        self.assertEqual(pkrcomponents.shape.Shape.PAIR, pkrcomponents.shape.Shape(""))
        self.assertEqual(pkrcomponents.shape.Shape.OFFSUIT, pkrcomponents.shape.Shape("o"))
        self.assertEqual(pkrcomponents.shape.Shape.SUITED, pkrcomponents.shape.Shape("s"))
        self.assertNotEqual(pkrcomponents.shape.Shape.PAIR, pkrcomponents.shape.Shape("s"))

    def test_name(self):
        self.assertEqual(pkrcomponents.shape.Shape.PAIR.name, "PAIR")
        self.assertEqual(pkrcomponents.shape.Shape.OFFSUIT.name, "OFFSUIT")
        self.assertEqual(pkrcomponents.shape.Shape.SUITED.name, "SUITED")

    def test_symbol(self):
        self.assertEqual(pkrcomponents.shape.Shape.PAIR.symbol, "")
        self.assertEqual(pkrcomponents.shape.Shape.OFFSUIT.symbol, "o")
        self.assertEqual(pkrcomponents.shape.Shape.SUITED.symbol, "s")

    def test_adjective(self):
        self.assertEqual(pkrcomponents.shape.Shape.PAIR.adjective, "paired")
        self.assertEqual(pkrcomponents.shape.Shape.OFFSUIT.adjective, "offsuit")
        self.assertEqual(pkrcomponents.shape.Shape.SUITED.adjective, "suited")


if __name__ == '__main__':
    unittest.main()
