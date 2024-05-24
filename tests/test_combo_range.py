import unittest
import pkrcomponents.hand as hand


class MyComboHandTestCase(unittest.TestCase):

    def test_all(self):
        self.assertIsInstance(hand.ComboRange(), hand.ComboRange)


if __name__ == '__main__':
    unittest.main()
