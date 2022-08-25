import unittest
import components.hand as hand


class MyTestCase(unittest.TestCase):

    def test_something(self):
        print(hand.Hand.make_random())

if __name__ == '__main__':
    unittest.main()
