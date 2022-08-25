import unittest
import components.hand as hand


class MyShapeTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.all_shapes = list(hand.Shape)

    def test_shapes_length(self):
        self.assertEqual(len(self.all_shapes), 3)


if __name__ == '__main__':
    unittest.main()
