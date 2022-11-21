import unittest
import pkrcomponents.lookup_table as lookup


class MyTestCase(unittest.TestCase):
    def test_something(self):
        lk_table = lookup.LookupTable()
        self.assertIsInstance(lk_table, lookup.LookupTable)


if __name__ == '__main__':
    unittest.main()
