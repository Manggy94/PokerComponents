import unittest
import pkrcomponents.tournament as tournament


class MyLevelTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.level = tournament.Level(8, 1600)

    def test_str(self):
        self.assertIsInstance(self.level.__str__(), str)

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
        lvl = tournament.Level(bb=200, ante=25)
        with self.assertRaises(ValueError):
            self.level.ante = -1
        self.assertEqual(self.level.ante, 200)
        self.assertEqual(lvl.ante, 25)
        lvl.ante = 24
        self.assertEqual(lvl.ante, 24)

    def test_level(self):
        with self.assertRaises(ValueError):
            self.level.level = -2
        with self.assertRaises(ValueError):
            self.level.level = 0.1
        self.assertEqual(self.level.level, 8)
        self.level.level = 11
        self.assertEqual(self.level.level, 11)

    def test_json(self):
        self.assertIsInstance(self.level.to_json(), dict)
        self.assertEqual(self.level.to_json()["level"], 8)
        self.assertEqual(self.level.to_json()["ante"], 200)
        self.assertEqual(self.level.to_json()["sb"], 800)
        self.assertEqual(self.level.to_json()["bb"], 1600)


if __name__ == '__main__':
    unittest.main()
