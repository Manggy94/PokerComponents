import unittest
from pkrcomponents.components.cards import LookupTable


class MyTestCase(unittest.TestCase):
    def test_something(self):
        lk_table = LookupTable()
        self.assertIsInstance(lk_table, LookupTable)


if __name__ == '__main__':
    unittest.main()
