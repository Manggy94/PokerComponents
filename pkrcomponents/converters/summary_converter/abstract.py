import json
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime


from pkrcomponents.components.tournaments.buy_in import BuyIn
from pkrcomponents.components.tournaments.speed import TourSpeed
from pkrcomponents.components.tournaments.tournament import Tournament
from pkrcomponents.components.tournaments.tournament_type import TournamentType
from pkrcomponents.converters.utils.exceptions import SummaryConversionError


class AbstractSummaryConverter(ABC):

    data: dict
    tournament: Tournament

    @abstractmethod
    def list_parsed_summaries_keys(self) -> list:
        """
        Lists all the parsed summary files.
        Returns:
            keys (list): A list of the keys of the parsed summary files
        """
        pass

    @abstractmethod
    def read_data_text(self, parsed_key: str) -> str:
        """
        Reads the data of a parsed history
        Args:
            parsed_key (str): The key of the parsed history
        Returns:
            data_text (str): The data text of the parsed history
        """
        pass

    def get_parsed_data(self, parsed_key: str):
        """
        Gets the data of a parsed history and stores it in the data attribute
        Args:
            parsed_key (str): The key of the parsed history
        """
        data_text = self.read_data_text(parsed_key)
        self.data = json.loads(data_text)

    def get_buy_in(self):
        """
        Get the buy in from the data and return a BuyIn object to set the tournament object

        Returns:
            buy_in (BuyIn): BuyIn object
        """
        freeze = self.data.get("buy_in").get("prize_pool_contribution")
        ko = self.data.get("buy_in").get("bounty")
        rake = self.data.get("buy_in").get("rake")
        buy_in = BuyIn(prize_pool=freeze, bounty=ko, rake=rake)
        self.tournament.buy_in = buy_in

    def get_registered_players(self):
        """
        Get the registered players from the data and set it to the set table object

        Returns:
            registered_players (int): Nb of registered players
        """
        registered_players = self.data.get("registered_players")
        self.tournament.total_players = registered_players

    def get_tournament_name(self):
        """
        Get the tournament name from the data and set it to set the tournament object

        Returns:
            tournament_name (str): Tournament name
        """
        tournament_name = self.data.get("tournament_name")
        self.tournament.name = tournament_name

    def get_tournament_id(self):
        """
        Get the tournament id from the data and set it to the set tournament object

        Returns:
            tournament_id (str): Tournament id
        """
        tournament_id = self.data.get("tournament_id")
        self.tournament.id = tournament_id

    def get_tournament_speed(self):
        """
        Get the tournament speed from the data and set it to the table object

        Returns:
            speed (str): Tournament speed
        """
        try:
            speed = TourSpeed(self.data.get("speed"))
        except ValueError:
            speed = TourSpeed.REGULAR
        self.tournament.speed = speed

    def get_tournament_start_date(self):
        """
        Get the tournament start date from the data and set it to the set table object

        Returns:
            start_date (str): Tournament start date
        """
        start_date_string = self.data.get("start_date")
        date_format = "%Y/%m/%d %H:%M:%S %Z"
        start_date = datetime.strptime(start_date_string, date_format)
        self.tournament.start_date = start_date

    def get_final_position(self):
        """
        Get the final position of the player in the tournament
        """
        final_position = self.data.get("final_position")
        self.tournament.final_position = final_position

    def get_amount_won(self):
        """
        Get the amount won by the player in the tournament
        """
        amount_won = self.data.get("amount_won")
        self.tournament.amount_won = amount_won

    def get_tournament_type(self):
        """
        Get the tournament type from the data and set it to the set table object
        """
        tournament_type = self.data.get("tournament_type")
        tournament_type = TournamentType(tournament_type)
        self.tournament.tournament_type = tournament_type

    def get_prize_pool(self):
        """
        Get the prize pool from the data and set it to the set table object
        """
        prize_pool = self.data.get("prize_pool")
        self.tournament.set_prize_pool(prize_pool)

    def get_nb_entries(self):
        """
        Get the number of entries from the data and set it to the set table object
        """
        nb_entries = self.data.get("nb_entries")
        self.tournament.nb_entries = nb_entries

    def get_levels_structure(self):
        # TODO: Implement this method taking a list of dictionaries and converting it to a LevelsStructure object
        pass

    def get_tournament(self):
        """
        Get the tournament data and set it to the set table object
        """
        try:
            self.get_tournament_name()
            self.get_tournament_id()
            self.get_buy_in()
            self.get_tournament_speed()
            self.get_registered_players()
            self.get_tournament_start_date()
            self.get_final_position()
            self.get_amount_won()
            self.get_tournament_type()
            self.get_prize_pool()
            self.get_nb_entries()
            self.get_levels_structure()
        except TypeError:
            print("Error converting tournament info data")
            raise SummaryConversionError

    def reset_tournament(self):
        self.tournament = Tournament()

    def convert_summary(self, parsed_key: str) -> Tournament:
        self.get_parsed_data(parsed_key)
        self.get_tournament()
        return self.tournament

    def convert_summaries(self):
        parsed_keys = self.list_parsed_summaries_keys()
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.convert_summary, parsed_key) for parsed_key in parsed_keys]
            for future in as_completed(futures):
                future.result()
