import unittest
import pkrcomponents.bitcard as bitcard


class MyBitCardTestCase(unittest.TestCase):
    def test_new_and_properties(self):
        bc = bitcard.BitCard("As")
        bc2 = bitcard.BitCard(bitcard.Card("Ks"))
        bc3 = bitcard.BitCard(33589533)
        bc4 = bitcard.BitCard("5c")
        self.assertIsInstance(bc, bitcard.BitCard)
        self.assertIsInstance(bc2, bitcard.BitCard)
        self.assertIsInstance(bc3, bitcard.BitCard)
        self.assertEqual(bc.rank, 12)
        self.assertEqual(bc.suit, 8)
        self.assertEqual(bc3.prime, 29)
        self.assertEqual(bc4.bitrank, 8)
        self.assertIsInstance(bc3.binary_string, str)
        self.assertEqual(bc4.binary_string, "0000\t0000\t0000\t1000\t0001\t0011\t0000\t0111")

    def test_cards_to_int(self):
        self.assertIsInstance(bitcard.BitCard.cards_to_int(("As", "Ad")), list)
        self.assertEqual(bitcard.BitCard.cards_to_int(("As", "Ad", "Jd")), [268471337, 268446761, 33564957])

    def test_prime_product_from_cards(self):
        self.assertIsInstance(bitcard.BitCard.prime_product_from_cards(("As", "Ad")), int)
        self.assertEqual(bitcard.BitCard.prime_product_from_cards(("2s", "3d", "4d")), 30)
        self.assertEqual(bitcard.BitCard.prime_product_from_cards(("As", "2d", "4d")), 41*2*5)


if __name__ == '__main__':
    unittest.main()
