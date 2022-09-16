import unittest
import components.hand as hand


class MyGeneralTestCase(unittest.TestCase):

    def test_all(self):
        self.assertIsInstance(hand.__all__, list)

    def test_suits_combinations(self):
        self.assertIsInstance(hand.__all__, list)

    def test_new_meta_hand(self):
        HM = hand._HandMeta()
        self.assertIsInstance(HM, hand._HandMeta)

if __name__ == '__main__':
    unittest.main()
