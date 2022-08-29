import unittest
import components.tournament as tournament


class MyTournamentTestCase(unittest.TestCase):

    def setUp(self):
        self.tour = tournament.Tournament("tour_id", name="PLD", money_type="real")

    def test_new_tournament(self):
        tour = tournament.Tournament()
        self.assertIsInstance(tour, tournament.Tournament)
        self.assertEqual(tour.id, "0000")
        self.assertEqual(tour.name, "Kill The Fish")


if __name__ == '__main__':
    unittest.main()
