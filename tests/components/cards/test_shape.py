import unittest
import pkrcomponents.components.cards.shape


class MyShapeTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.all_shapes = list(pkrcomponents.components.cards.shape.Shape)

    def test_shapes_length(self):
        self.assertEqual(len(self.all_shapes), 3)

    def test_shapes_contains(self):
        self.assertIn(pkrcomponents.components.cards.shape.Shape(""), self.all_shapes)
        self.assertIn(pkrcomponents.components.cards.shape.Shape("s"), self.all_shapes)
        self.assertIn(pkrcomponents.components.cards.shape.Shape("o"), self.all_shapes)

    def test_shape_values(self):
        self.assertEqual(pkrcomponents.components.cards.shape.Shape.PAIR, pkrcomponents.components.cards.shape.Shape(""))
        self.assertEqual(pkrcomponents.components.cards.shape.Shape.OFFSUIT, pkrcomponents.components.cards.shape.Shape("o"))
        self.assertEqual(pkrcomponents.components.cards.shape.Shape.SUITED, pkrcomponents.components.cards.shape.Shape("s"))
        self.assertNotEqual(pkrcomponents.components.cards.shape.Shape.PAIR, pkrcomponents.components.cards.shape.Shape("s"))

    def test_name(self):
        self.assertEqual(pkrcomponents.components.cards.shape.Shape.PAIR.name, "PAIR")
        self.assertEqual(pkrcomponents.components.cards.shape.Shape.OFFSUIT.name, "OFFSUIT")
        self.assertEqual(pkrcomponents.components.cards.shape.Shape.SUITED.name, "SUITED")

    def test_symbol(self):
        self.assertEqual(pkrcomponents.components.cards.shape.Shape.PAIR.symbol, "")
        self.assertEqual(pkrcomponents.components.cards.shape.Shape.OFFSUIT.symbol, "o")
        self.assertEqual(pkrcomponents.components.cards.shape.Shape.SUITED.symbol, "s")

    def test_adjective(self):
        self.assertEqual(pkrcomponents.components.cards.shape.Shape.PAIR.adjective, "paired")
        self.assertEqual(pkrcomponents.components.cards.shape.Shape.OFFSUIT.adjective, "offsuit")
        self.assertEqual(pkrcomponents.components.cards.shape.Shape.SUITED.adjective, "suited")


if __name__ == '__main__':
    unittest.main()
