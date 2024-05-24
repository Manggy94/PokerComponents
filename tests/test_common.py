import unittest
import pkrcomponents._common as common


class MyCommonTestCase(unittest.TestCase):
    def test_new_class(self):
        with self.assertRaises(TypeError):
            class TOTO(common.PokerEnum):
                VALID = 1, 2, 3
                INVALID = 1


if __name__ == '__main__':
    unittest.main()
