import unittest
from pkrcomponents.components.actions.blind_type import BlindType


class BlindTypeTest(unittest.TestCase):

    def test_name(self):
        self.assertEqual(BlindType.BIG_BLIND.name, "BIG_BLIND")
        self.assertEqual(BlindType.SMALL_BLIND.name, "SMALL_BLIND")
        self.assertEqual(BlindType.ANTE.name, "ANTE")

    def test_symbol(self):
        self.assertEqual(BlindType.BIG_BLIND.symbol, "BB")
        self.assertEqual(BlindType.SMALL_BLIND.symbol, "SB")
        self.assertEqual(BlindType.ANTE.symbol, "A")
