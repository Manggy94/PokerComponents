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


if __name__ == '__main__':
    unittest.main()
