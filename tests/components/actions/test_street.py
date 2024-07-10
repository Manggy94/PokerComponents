
import unittest
from pkrcomponents.components.actions.street import Street


class StreetTest(unittest.TestCase):

    def test_is_preflop(self):
        self.assertTrue(Street.PREFLOP.is_preflop)
        self.assertFalse(Street.FLOP.is_preflop)
        self.assertFalse(Street.TURN.is_preflop)
        self.assertFalse(Street.RIVER.is_preflop)
        self.assertFalse(Street.SHOWDOWN.is_preflop)

    def test_symbol(self):
        self.assertEqual(Street.PREFLOP.symbol, 'PF')
        self.assertEqual(Street.FLOP.symbol, 'F')
        self.assertEqual(Street.TURN.symbol, 'T')
        self.assertEqual(Street.RIVER.symbol, 'R')
        self.assertEqual(Street.SHOWDOWN.symbol, 'SD')

    def test_name(self):
        self.assertEqual(Street.PREFLOP.name, 'PREFLOP')
        self.assertEqual(Street.FLOP.name, 'FLOP')
        self.assertEqual(Street.TURN.name, 'TURN')
        self.assertEqual(Street.RIVER.name, 'RIVER')
        self.assertEqual(Street.SHOWDOWN.name, 'SHOWDOWN')

    def test_parsing_name(self):
        self.assertEqual(Street.PREFLOP.parsing_name, 'PreFlop')
        self.assertEqual(Street.FLOP.parsing_name, 'Flop')
        self.assertEqual(Street.TURN.parsing_name, 'Turn')
        self.assertEqual(Street.RIVER.parsing_name, 'River')
        self.assertEqual(Street.SHOWDOWN.parsing_name, 'ShowDown')

    def test_short_name(self):
        self.assertEqual(Street.PREFLOP.short_name, 'PF')
        self.assertEqual(Street.FLOP.short_name, 'F')
        self.assertEqual(Street.TURN.short_name, 'T')
        self.assertEqual(Street.RIVER.short_name, 'R')
        self.assertEqual(Street.SHOWDOWN.short_name, 'SD')

