import unittest
import pkrcomponents.tournament as tournament
import pkrcomponents.constants as cst


class MyTournamentTestCase(unittest.TestCase):

    def setUp(self):
        self.tour = tournament.Tournament("tour_id", name="PLD", money_type="real", buyin=9.5)
        self.level = tournament.Level()
        self.level2 = tournament.Level(level=4, bb=600)

    def test_new_tournament(self):
        tour = tournament.Tournament(level=self.level)
        self.assertIsInstance(tour, tournament.Tournament)
        self.assertIsInstance(tour.level, tournament.Level)
        self.assertEqual(tour.id, "0000")
        self.assertEqual(tour.name, "Kill The Fish")
        self.assertEqual(tour.is_ko, True)
        tour.is_ko = False
        self.assertEqual(tour.is_ko, False)
        tour.level = self.level2

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

    def test_to_json(self):
        self.assertIsInstance(self.tour.to_json(), dict)
        self.assertEqual(self.tour.to_json(), {
            'level': {
                'level': 1,
                'ante': 25.0,
                'sb': 100.0,
                'bb': 200.0
            },
            'id': 'tour_id',
            'name': 'PLD',
            'buy_in': 9.5,
            'is_ko': True,
            'money_type': cst.MoneyType('Real money')})


if __name__ == '__main__':
    unittest.main()
