import unittest
from pkrcomponents.pot import Pot


class MyPotTestCase(unittest.TestCase):
    def test_new_pot(self):
        p = Pot()
        self.assertIsInstance(p, Pot)
        with self.assertRaises(ValueError):
            p.value = -10
        self.assertEqual(p.value, 0)

    def test_add(self):
        p = Pot()
        with self.assertRaises(ValueError):
            p.add(-10)
        p.add(2500)
        self.assertEqual(p.value, 2500)
        p.add(500)
        self.assertEqual(p.value, 3000)

    def test_reset(self):
        p = Pot()
        p.add(2500)
        p.reset()
        self.assertEqual(p.value, 0)
        self.assertEqual(p.highest_bet, 0)



if __name__ == '__main__':
    unittest.main()
