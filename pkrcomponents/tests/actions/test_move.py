from unittest import TestCase

from pkrcomponents.models.actions.move import Move


class TestMove(TestCase):
    """
    Test the Move model
    """
    def setUp(self):
        """
        Set up the test by getting the Move objects from the database
        """
        self.move = Move("FOLD", "F", "folds")
        self.move2 = Move("CALL", "C", "calls")
        self.move3 = Move("RAISE", "R", "raises")
        self.move4 = Move("BET", "B", "bets")
        self.move5 = Move("CHECK", "X", "checks")

    def test_move_name(self):
        """
        Test the name of the Move objects
        """
        self.assertIsInstance(self.move.name, str)
        self.assertEqual(self.move.name, 'FOLD')
        self.assertEqual(self.move2.name, 'CALL')
        self.assertEqual(self.move3.name, 'RAISE')
        self.assertEqual(self.move4.name, 'BET')
        self.assertEqual(self.move5.name, 'CHECK')

    def test_move_symbol(self):
        """
        Test the symbol of the Move objects
        """
        self.assertIsInstance(self.move.symbol, str)
        self.assertEqual(self.move.symbol, 'F')
        self.assertEqual(self.move2.symbol, 'C')
        self.assertEqual(self.move3.symbol, 'R')
        self.assertEqual(self.move4.symbol, 'B')
        self.assertEqual(self.move5.symbol, 'X')

    def test_move_verb(self):
        """
        Test the verb of the Move objects (for parsing
        """
        self.assertIsInstance(self.move.verb, str)
        self.assertEqual(self.move.verb, 'folds')
        self.assertEqual(self.move2.verb, 'calls')
        self.assertEqual(self.move3.verb, 'raises')
        self.assertEqual(self.move4.verb, 'bets')
        self.assertEqual(self.move5.verb, 'checks')

    def test_move_is_call_move(self):
        """
        Test the is_call_move property of the Move objects
        """
        self.assertIsInstance(self.move.is_call_move, bool)
        self.assertEqual(self.move.is_call_move, False)
        self.assertEqual(self.move2.is_call_move, True)
        self.assertEqual(self.move3.is_call_move, False)
        self.assertEqual(self.move4.is_call_move, False)
        self.assertEqual(self.move5.is_call_move, True)

    def test_move_is_bet_move(self):
        """
        Test the is_bet_move property of the Move objects
        """
        self.assertIsInstance(self.move.is_bet_move, bool)
        self.assertEqual(self.move.is_bet_move, False)
        self.assertEqual(self.move2.is_bet_move, False)
        self.assertEqual(self.move3.is_bet_move, True)
        self.assertEqual(self.move4.is_bet_move, True)
        self.assertEqual(self.move5.is_bet_move, False)

    def test_move_is_vpip_move(self):
        """
        Test the is_vpip_move property of the Move objects
        """
        self.assertIsInstance(self.move.is_vpip_move, bool)
        self.assertEqual(self.move.is_vpip_move, False)
        self.assertEqual(self.move2.is_vpip_move, True)
        self.assertEqual(self.move3.is_vpip_move, True)
        self.assertEqual(self.move4.is_vpip_move, True)
        self.assertEqual(self.move5.is_vpip_move, False)
