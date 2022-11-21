import unittest
import pkrcomponents.constants as cst


class MyConstantsTestCase(unittest.TestCase):
    def test_pkr_room(self):
        room1 = cst.PokerRoom.WINA
        room2 = cst.PokerRoom.PKR
        room3 = cst.PokerRoom("Winamax")
        self.assertFalse(room1 == room2)
        self.assertTrue(room1 == room3)
        with self.assertRaises(ValueError):
            room1 == cst.GameType.TOUR
        with self.assertRaises(ValueError):
            room1 < cst.GameType.TOUR


if __name__ == '__main__':
    unittest.main()
