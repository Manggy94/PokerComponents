import unittest
import components.tournament as tournament
import components.constants as cst


class MyTournamentTestCase(unittest.TestCase):

    def setUp(self):
        self.tour = tournament.Tournament("tour_id", name="PLD", money_type="real", buyin=9.5)

    def test_new_tournament(self):
        tour = tournament.Tournament()
        self.assertIsInstance(tour, tournament.Tournament)
        self.assertEqual(tour.id, "0000")
        self.assertEqual(tour.name, "Kill The Fish")

    def test_str(self):
        self.assertIsInstance(self.tour.__str__(), str)

    def test_id_and_type(self):
        self.assertIsInstance(self.tour.id, str)
        self.assertEqual(self.tour.id, "tour_id")
        self.tour.id = "None"
        self.assertEqual(self.tour.id, "None")
        self.assertIsInstance(self.tour.money_type, cst.MoneyType)
        self.assertEqual(self.tour.money_type, cst.MoneyType.REAL)
        self.tour.money_type = "play"
        self.assertEqual(self.tour.money_type, cst.MoneyType.PLAY)

    def test_name(self):
        self.assertIsInstance(self.tour.name, str)
        self.assertEqual(self.tour.name, "PLD")
        self.tour.name = "Name"
        self.assertEqual(self.tour.name, "Name")

    def test_buyin(self):
        self.assertIsInstance(self.tour.buyin, float)
        self.assertEqual(self.tour.buyin, 9.5)
        self.tour.buyin = 10.0
        self.assertEqual(self.tour.buyin, 10)


if __name__ == '__main__':
    unittest.main()
