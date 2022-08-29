import unittest
import components.street as street


class MyStreetTestCase(unittest.TestCase):

    def setUp(self):
        self.street = street.Street()

    def test_new_street(self):
        self.assertIsInstance(self.street, street.Street)
        self.assertRaises(ValueError, lambda: street.Street("Coca-Cola"))



if __name__ == '__main__':
    unittest.main()
