from unittest import TestCase

from pkrcomponents.models.actions.street import Street


class TestStreet(TestCase):
    """
    Test the Street model
    """
    def setUp(self):
        """
        Set up the test by getting the Street objects from the database
        """
        self.street = Street("PREFLOP")
        self.street2 = Street("FLOP")
        self.street3 = Street("TURN")
        self.street4 = Street("RIVER")

    def test_street_name(self):
        """
        Test the name of the Street objects
        """
        self.assertIsInstance(self.street.name, str)
        self.assertEqual(self.street.name, 'PREFLOP')
        self.assertEqual(self.street2.name, 'FLOP')
        self.assertEqual(self.street3.name, 'TURN')
        self.assertEqual(self.street4.name, 'RIVER')

    def test_street_symbol(self):
        """
        Test the symbol of the Street objects
        """
        self.assertIsInstance(self.street.symbol, str)
        self.assertEqual(self.street.symbol, 'P')
        self.assertEqual(self.street2.symbol, 'F')
        self.assertEqual(self.street3.symbol, 'T')
        self.assertEqual(self.street4.symbol, 'R')

    def test_street_short_name(self):
        """
        Test the short_name of the Street objects
        """
        self.assertIsInstance(self.street.short_name, str)
        self.assertEqual(self.street.short_name, 'Preflop')
        self.assertEqual(self.street2.short_name, 'Flop')
        self.assertEqual(self.street3.short_name, 'Turn')
        self.assertEqual(self.street4.short_name, 'River')

    def test_street_order(self):
        """
        Test the order of the Street objects
        """
        self.assertIsInstance(self.street.order, int)
        self.assertEqual(self.street.order, 1)
        self.assertEqual(self.street2.order, 2)
        self.assertEqual(self.street3.order, 3)
        self.assertEqual(self.street4.order, 4)
