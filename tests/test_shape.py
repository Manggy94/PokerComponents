import unittest
import pkrcomponents.cards.shape


class MyShapeTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.all_shapes = list(pkrcomponents.cards.shape.Shape)

    def test_shapes_length(self):
        self.assertEqual(len(self.all_shapes), 3)

    def test_shapes_contains(self):
        self.assertIn(pkrcomponents.cards.shape.Shape(""), self.all_shapes)
        self.assertIn(pkrcomponents.cards.shape.Shape("s"), self.all_shapes)
        self.assertIn(pkrcomponents.cards.shape.Shape("o"), self.all_shapes)

    def test_shape_values(self):
        self.assertEqual(pkrcomponents.cards.shape.Shape.PAIR, pkrcomponents.cards.shape.Shape(""))
        self.assertEqual(pkrcomponents.cards.shape.Shape.OFFSUIT, pkrcomponents.cards.shape.Shape("o"))
        self.assertEqual(pkrcomponents.cards.shape.Shape.SUITED, pkrcomponents.cards.shape.Shape("s"))
        self.assertNotEqual(pkrcomponents.cards.shape.Shape.PAIR, pkrcomponents.cards.shape.Shape("s"))

    def test_name(self):
        self.assertEqual(pkrcomponents.cards.shape.Shape.PAIR.name, "PAIR")
        self.assertEqual(pkrcomponents.cards.shape.Shape.OFFSUIT.name, "OFFSUIT")
        self.assertEqual(pkrcomponents.cards.shape.Shape.SUITED.name, "SUITED")

    def test_symbol(self):
        self.assertEqual(pkrcomponents.cards.shape.Shape.PAIR.symbol, "")
        self.assertEqual(pkrcomponents.cards.shape.Shape.OFFSUIT.symbol, "o")
        self.assertEqual(pkrcomponents.cards.shape.Shape.SUITED.symbol, "s")

    def test_adjective(self):
        self.assertEqual(pkrcomponents.cards.shape.Shape.PAIR.adjective, "paired")
        self.assertEqual(pkrcomponents.cards.shape.Shape.OFFSUIT.adjective, "offsuit")
        self.assertEqual(pkrcomponents.cards.shape.Shape.SUITED.adjective, "suited")


if __name__ == '__main__':
    unittest.main()
