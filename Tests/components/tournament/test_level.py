import unittest
import components.tournament as tournament


class MyLevelTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.level = tournament.Level(8, 1600)

    def test_new_level(self):
        self.assertIsInstance(self.level, tournament.Level)
        self.assertIsInstance(self.level.level, int)
        self.assertIsInstance(self.level._sb, float)
        self.assertIsInstance(self.level._bb, float)
        self.assertIsInstance(self.level._ante, float)

    def test_bb(self):
        with self.assertRaises(ValueError):
            self.level.bb = -1
        self.assertEqual(self.level.bb, 1600)
        self.assertEqual(self.level.sb, 800)

    def test_ante(self):
        with self.assertRaises(ValueError):
            self.level.ante = -1
        self.assertEqual(self.level.ante, 200)

    def test_level(self):
        with self.assertRaises(ValueError):
            self.level.level = -2
        with self.assertRaises(ValueError):
            self.level.level = 0.1
        self.assertEqual(self.level.level, 8)


if __name__ == '__main__':
    unittest.main()
