import json
from datetime import datetime
from pkrcomponents.components.actions.action import CallAction, BetAction, RaiseAction, FoldAction, CheckAction
from pkrcomponents.components.actions.action_move import ActionMove
from pkrcomponents.components.actions.street import Street
from pkrcomponents.components.cards.combo import Combo
from pkrcomponents.components.players.table_player import TablePlayer
from pkrcomponents.components.tables.table import Table
from pkrcomponents.components.tournaments.buy_in import BuyIn
from pkrcomponents.components.tournaments.level import Level
from pkrcomponents.components.tournaments.speed import TourSpeed
from pkrcomponents.components.tournaments.tournament import Tournament
from pkrcomponents.components.utils.exceptions import (ShowdownNotReachedError, CannotParseWinnersError,
                                                       NotSufficientBetError, NotSufficientRaiseError,
                                                       EmptyButtonSeatError)

from pkrcomponents.history_converter.utils.exceptions import HandConversionError


class HandHistoryConverter:
    """
    Class to convert a hand history into a table object

    Attributes:
        data (dict): Data from the hand history file
        table (Table): Table object to set the data to

    Methods:
        get_data: Get the data from a hand history file
        get_max_players: Get the max players from the data and set it to the table object
        get_buy_in: Get the buy in from the data and return a BuyIn object to set the tournament object
        get_level: Get the level  and blinds from the data and set it to set the tournament object
        get_tournament_name: Get the tournament name from the data and set it to set the tournament object
        get_tournament_id: Get the tournament id from the data and set it to the set tournament object
        get_table_number: Get the table number from the data and set it to the set tournament object
        get_tournament: Get the tournament data and set it to the set table object
        get_hand_id: Get the hand id from the data and set it to the set table object
        get_datetime: Get the datetime from the data and set it to the set table object
        get_game_type: Get the game type from the data and set it to the set table object
        get_button_seat: Get the button seat from the data and set it to the set table object
        get_players: Get the players from the data and set them to the set table object
        get_player: Get a player from the data and set it to the set table object
        get_postings: Get the postings from the data and set them to the set table object
        get_actions: Get the actions from the data and set them to the table object
        get_street_actions: Get the actions from a street from the data and set them to the table object
        get_action: Get an action from the data and set it to the table object
        get_flop: Get the flop cards from the data and set them to the table object
        get_turn: Get the turn card from the data and set it to the table object
        get_river: Get the river card from the data and set it to the table object
        get_showdown: Get the showdown data from the data and set it to the table object
        get_winners: Get the winners data from the data and set it to the table object
        advance_street: Advance to the next street
        convert_history: Convert a hand history file into a table object


    """

    data: dict

    def __init__(self):
        self.table = Table()

    def get_data(self, file_path: str):
        """
        Get the data from a hand history file

        Args:
            file_path (str): Path to the hand history file
        """
        with open(file_path, 'r') as file:
            data = json.load(file)
        self.data = data

    def get_max_players(self):
        """Get the max players from the data and set it to the table object"""
        max_players = self.data.get("max_players")
        self.table.set_max_players(max_players)

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
        return buy_in

    def get_level(self) -> Level:
        """
        Get the level  and blinds from the data and set it to set the tournament object

        Returns:
            level (Level): Level object
        """
        level_data = self.data.get("level")
        level = Level(value=level_data.get("value"), bb=level_data.get("bb"), ante=level_data.get("ante"))
        return level

    def get_tournament_name(self) -> str:
        """
        Get the tournament name from the data and set it to set the tournament object

        Returns:
            tournament_name (str): Tournament name
        """
        tournament_name = self.data.get("tournament_info").get("tournament_name")
        return tournament_name

    def get_tournament_id(self):
        """
        Get the tournament id from the data and set it to the set tournament object

        Returns:
            tournament_id (str): Tournament id
        """
        tournament_id = self.data.get("tournament_info").get("tournament_id")
        return tournament_id

    def get_table_number(self) -> str:
        """
        Get the table number from the data and set it to the set tournament object

        Returns:
            table_number (str): Table number
        """
        table_number = self.data.get("tournament_info").get("table_number")
        return table_number

    def get_tournament(self):
        """
        Get the tournament data and set it to the set table object
        """
        try:
            tournament_name = self.get_tournament_name()
            tournament_id = self.get_tournament_id()
            buy_in = self.get_buy_in()
            level = self.get_level()
            speed = self.get_tournament_speed()
            total_players = self.get_registered_players()
            start_date = self.get_tournament_start_date()
            tournament = Tournament(name=tournament_name, id=tournament_id, buy_in=buy_in, level=level, speed=speed,
                                    total_players=total_players, start_date=start_date)
            self.table.add_tournament(tournament)
        except TypeError:
            print("Error converting tournament info data")
            raise HandConversionError

    def get_hand_id(self):
        """
        Get the hand id from the data and set it to the table object
        """
        self.table.hand_id = self.data.get("hand_id")

    def get_datetime(self):
        """
        Get the datetime from the data and set it to the table object
        """
        hand_date_str = self.data.get("datetime")
        date_format = "%d-%m-%Y %H:%M:%S"
        hand_datetime = datetime.strptime(hand_date_str, date_format)
        self.table.hand_date = hand_datetime

    def get_tournament_speed(self) -> str:
        """
        Get the tournament speed from the data and set it to the table object

        Returns:
            speed (str): Tournament speed
        """
        try:
            speed = TourSpeed(self.data.get("tournament_info").get("speed"))
        except ValueError:
            speed = TourSpeed.REGULAR
        return speed

    def get_registered_players(self) -> int:
        """
        Get the registered players from the data and set it to the set table object

        Returns:
            registered_players (int): Nb of registered players
        """
        registered_players = self.data.get("tournament_info").get("registered_players")
        return registered_players

    def get_tournament_start_date(self):
        """
        Get the tournament start date from the data and set it to the set table object

        Returns:
            start_date (str): Tournament start date
        """
        start_date_string = self.data.get("tournament_info").get("start_date")
        date_format = "%Y/%m/%d %H:%M:%S %Z"
        start_date = datetime.strptime(start_date_string, date_format)
        return start_date

    def get_game_type(self) -> str:
        """
        Get the game type from the data and set it to the set table object

        Returns:
            game_type (str): Game type
        """
        game_type = self.data.get("game_type")
        return game_type

    def get_button_seat(self):
        """
        Get the button seat from the data and set it to the set table object

        Returns:
            button_seat (int): Button seat
        """
        button_seat = self.data.get("button_seat")
        return button_seat

    def get_players(self):
        """Get the players from the data and set them to the set table object"""
        try:
            players_dict = self.data.get("players")
            for seat, player_dict in players_dict.items():
                self.get_player(player_dict)
            button_seat = self.get_button_seat()
            bb_seat = self.table.players.get_bb_seat_from_button(button_seat)
            self.table.set_bb_seat(bb_seat)
            self.table.players.distribute_positions()
        except EmptyButtonSeatError:
            print("Error converting players data: Empty button seat")
            raise HandConversionError

    def get_player(self, player_dict: dict):
        """
        Get a player from the data and set it to the set table object

        Args:
            player_dict (dict): Player data

        """
        seat = player_dict.get("seat")
        name = player_dict.get("name")
        init_stack = player_dict.get("init_stack")
        bounty = player_dict.get("bounty")
        player = TablePlayer(name=name, seat=seat, init_stack=init_stack, bounty=bounty)
        # self.table.add_player(player)
        player.sit(self.table)

    def get_hero(self):
        """Get the hero from the data and set it to the table object"""
        name = self.data.get("hero_hand").get("hero")
        first_card = self.data.get("hero_hand").get("first_card")
        second_card = self.data.get("hero_hand").get("second_card")
        if first_card and second_card:
            self.table.distribute_hero_cards(name, first_card, second_card)

    def get_postings(self):
        """
        Get the postings from the data and set them to the table object
        """
        self.table.start_hand()

    def get_actions(self):
        """
        Get the actions from the data and set them to the table object
        """
        actions_dict = self.data.get("actions")
        for street, actions in actions_dict.items():
            if not self.table.hand_ended:
                self.get_street_actions(street)

    def get_street_actions(self, street: Street):
        """
        Get the actions from a street from the data and set them to the table object

        Args:
            street (Street): Street to get the actions from
        """
        actions = self.data.get("actions").get(street)
        for action_dict in actions:
            self.get_action(action_dict)
        if self.table.next_street_ready:
            self.advance_street()

    def get_action(self, action_dict: dict):
        """
        Get an action from the data and set it to the table object

        Args:
            action_dict (dict): Action data
        """
        try:
            player = self.table.players[action_dict.get("player")]
            move = ActionMove(action_dict.get("action"))
            if move == ActionMove.FOLD:
                action = FoldAction(player)
            elif move == ActionMove.CHECK:
                action = CheckAction(player)
            elif move == ActionMove.CALL:
                action = CallAction(player)
            elif move == ActionMove.BET:
                amount = action_dict.get("amount")
                action = BetAction(player, amount)
            else:
                amount = action_dict.get("amount")
                action = RaiseAction(player, amount)
            action.play()
        except (NotSufficientBetError, NotSufficientRaiseError):
            print("Error converting actions data: Not sufficient bet or raise")
            raise HandConversionError

    def get_flop(self):
        """
        Get the flop cards from the data and set them to the table object
        """
        flop = self.data.get("flop")
        flop_card_1 = flop.get("flop_card_1")
        flop_card_2 = flop.get("flop_card_2")
        flop_card_3 = flop.get("flop_card_3")
        self.table.execute_flop(flop_card_1, flop_card_2, flop_card_3)

    def get_turn(self):
        """
        Get the turn card from the data and set it to the table object
        """
        turn = self.data.get("turn")
        turn_card = turn.get("turn_card")
        self.table.execute_turn(turn_card)

    def get_river(self):
        """
        Get the river card from the data and set it to the table object
        """
        river = self.data.get("river")
        river_card = river.get("river_card")
        self.table.execute_river(river_card)

    def get_showdown(self):
        """
        Get the showdown data from the data and set it to the table object

        """
        showdown_dict = self.data.get("showdown")
        try:
            for player_name, hand_dict in showdown_dict.items():
                player = self.table.players[player_name]
                first_card = hand_dict.get("first_card")
                second_card = hand_dict.get("second_card")
                combo = Combo.from_cards(first_card, second_card)
                player.shows(combo)
        except ShowdownNotReachedError:
            print("Error converting showdown data: Showdown not reached")
            raise HandConversionError
        except KeyError:
            print("Error converting showdown data: Key error")
            raise HandConversionError

    def get_winners(self):
        """
        Get the winners data from the data and set it to the table object
        """
        try:
            self.table.calculate_and_distribute_rewards()
        except (CannotParseWinnersError, ValueError):
            print("Error converting winners data: Cannot parse winners")
            raise HandConversionError

    def advance_street(self):
        """
        Advance to the next street
        """
        if self.table.street == Street.PREFLOP:
            self.get_flop()
        elif self.table.street == Street.FLOP:
            self.get_turn()
        elif self.table.street == Street.TURN:
            self.get_river()
        else:
            self.table.advance_to_showdown()

    def get_table_info(self):
        """
        Get the table info from the data and set it to the table object
        """
        self.get_hand_id()
        self.get_datetime()

    def convert_history(self, file_path: str) -> Table:
        """
        Convert a hand history file into a table object

        Args:
            file_path (str): Path to the hand history file

        Returns:
            (Table): Table object
        """
        try:
            self.get_data(file_path)
            self.get_table_info()
            self.get_tournament()
            self.get_max_players()
            self.get_players()
            self.get_hero()
            self.get_postings()
            self.get_actions()
            self.get_showdown()
            self.get_winners()
            return self.table
        except HandConversionError:
            print(f" Hand Conversion Error for file {file_path}")
            raise HandConversionError
        except ValueError:
            print(f"Error for file {file_path}")
            raise ValueError
        except TypeError:
            print(f"Error for file {file_path}")
            raise TypeError
