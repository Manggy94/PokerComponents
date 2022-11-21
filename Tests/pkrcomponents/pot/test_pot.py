import unittest
import pkrcomponents.pot as pot


class MyPotTestCase(unittest.TestCase):
    def test_new_pot(self):
        p = pot.Pot()
        self.assertIsInstance(p, pot.Pot)
        self.assertEqual(p.value, 0)

    def test_add(self):
        p = pot.Pot()
        self.assertRaises(ValueError, lambda: p.add(-10))
        p.add(2500)
        self.assertEqual(p.value, 2500)
        p.add(500)
        self.assertEqual(p.value, 3000)


if __name__ == '__main__':
    unittest.main()
