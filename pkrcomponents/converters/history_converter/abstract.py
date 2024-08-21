import json

from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from tqdm import tqdm

from pkrcomponents.components.actions.action import BetAction, CallAction, CheckAction, FoldAction, RaiseAction
from pkrcomponents.components.actions.action_move import ActionMove
from pkrcomponents.components.actions.blind_type import BlindType
from pkrcomponents.components.actions.posting import AntePosting, BBPosting, SBPosting
from pkrcomponents.components.actions.street import Street
from pkrcomponents.components.cards.combo import Combo
from pkrcomponents.components.players.table_player import TablePlayer
from pkrcomponents.components.tables.table import Table
from pkrcomponents.components.tournaments.level import Level
from pkrcomponents.components.tournaments.tournament import Tournament
from pkrcomponents.components.utils.exceptions import NotSufficientBetError, NotSufficientRaiseError, \
    ShowdownNotReachedError, CannotParseWinnersError, SeatTakenError, PlayerAlreadyFoldedError, \
    PlayerNotOnTableError
from pkrcomponents.converters.utils.exceptions import HandConversionError


class AbstractHandHistoryConverter(ABC):

    data: dict
    table: Table

    @abstractmethod
    def list_parsed_histories_keys(self) -> list:
        """
        Lists the keys of the parsed histories
        Returns:
            keys (list): The keys of the parsed histories
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

    @staticmethod
    def get_split_key(file_key: str) -> str:
        """
        Returns the key of the split history file from the parsed history file key
        """
        split_key = file_key.replace("parsed", "split").replace(".json", ".txt")
        return split_key

    @abstractmethod
    def send_to_corrections(self, file_key: str):
        """
        Moves the file to the corrections directory
        """
        pass

    def move_to_correction_dir(self, parsed_key: str):
        """
        Moves the parsed history file and the associated split file to the corrections directory
        """
        split_key = self.get_split_key(parsed_key)
        self.send_to_corrections(parsed_key)
        self.send_to_corrections(split_key)

    def get_max_players(self):
        """Get the max players from the data and set it to the table object"""
        max_players = self.data.get("max_players")
        self.table.set_max_players(max_players)

    def get_buy_in(self):
        """
        Get the total buy_in value from data and returns it

        Returns:
            buy_in (float): The total_buy_in amount
        """
        buy_in = self.data.get("buy_in")
        self.table.set_total_buy_in(buy_in)

    def get_level(self):
        """
        Get the level  and blinds from the data and set it to set the tournament object
        """
        level_data = self.data.get("level")
        level = Level(value=level_data.get("value"), bb=level_data.get("bb"), ante=level_data.get("ante"))
        self.table.set_level(level)

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

    def get_pregame_info(self):
        """
        Get the pregame info from the data and set it to the set table object
        """
        self.get_level()
        tournament_name = self.get_tournament_name()
        tournament_id = self.get_tournament_id()
        tournament = Tournament(name=tournament_name, id=tournament_id, level=self.table.level)
        self.table.add_tournament(tournament)
        self.get_table_number()
        self.get_max_players()
        self.get_buy_in()

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
        players_dict = self.data.get("players")
        for seat, player_dict in players_dict.items():
            self.get_player(player_dict)
        button_seat = self.get_button_seat()
        bb_seat = self.table.players.get_bb_seat_from_button(button_seat)
        self.table.set_bb_seat(bb_seat)
        self.table.players.distribute_positions()
        # self.table.players.delete_inactive_players()

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
        entered_hand = player_dict.get("entered_hand")
        player = TablePlayer(name=name, seat=seat, init_stack=init_stack, bounty=bounty, entered_hand=entered_hand)
        try:
            if entered_hand:
                player.sit(self.table)
        except SeatTakenError:
            player.replace(self.table)

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
        postings_list = self.data.get("postings")

        self.adapt_positions(postings_list)
        self.table.set_starting_status()
        for posting in postings_list:
            player = self.table.players[posting.get("name")]
            amount = posting.get("amount")
            blind_type = BlindType(posting.get("blind_type"))
            match blind_type:
                case BlindType.ANTE:
                    posting = AntePosting(player_name=player.name, value=amount)
                case BlindType.SMALL_BLIND:
                    posting = SBPosting(player_name=player.name, value=amount)
                case BlindType.BIG_BLIND:
                    posting = BBPosting(player_name=player.name, value=amount)
            posting.execute(player)

    def adapt_positions(self, postings_list: list):
        """
        Adapt the positions of the players according to the postings
        """
        for posting in postings_list:
            player = self.table.players[posting.get("name")]
            if posting.get("blind_type") == "big blind":
                self.table.players.bb_seat = player.seat
        # self.table.players.delete_inactive_players()
        self.table.players.distribute_positions()

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
        # print(self.table.street)
        actions = self.data.get("actions").get(street)
        for action_dict in actions:
            # print(action_dict)
            self.get_action(action_dict)
        # print(self.table.street_ended)
        # print(self.table.players)
        if self.table.next_street_ready:
            self.advance_street()

    def get_action(self, action_dict: dict):
        """
        Get an action from the data and set it to the table object

        Args:
            action_dict (dict): Action data
        """
        player = self.table.players[action_dict.get("player")]
        is_all_in = action_dict.get("is_all_in")
        if player.folded:
            raise PlayerAlreadyFoldedError
        move = ActionMove(action_dict.get("action"))
        match move:
            case ActionMove.FOLD:
                action = FoldAction(player)
            case ActionMove.CHECK:
                action = CheckAction(player)
            case ActionMove.CALL:
                action = CallAction(player, is_all_in=is_all_in)
            case ActionMove.BET:
                amount = action_dict.get("amount")
                action = BetAction(player, amount, is_all_in=is_all_in)
            case ActionMove.RAISE:
                amount = action_dict.get("amount")
                action = RaiseAction(player, amount, is_all_in=is_all_in)
            case other:
                raise ValueError(f"Invalid action: {other}")
        action.play()

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
        for player_name, hand_dict in showdown_dict.items():
            player = self.table.players[player_name]
            first_card = hand_dict.get("first_card")
            second_card = hand_dict.get("second_card")
            combo = Combo.from_cards(first_card, second_card)
            player.shows(combo)

    def get_winners(self):
        """
        Get the winners data from the data and set it to the table object
        """
        self.table.calculate_and_distribute_rewards()

    def advance_street(self):
        """
        Advance to the next street
        """
        match self.table.street:
            case Street.PREFLOP:
                self.get_flop()
            case Street.FLOP:
                self.get_turn()
            case Street.TURN:
                self.get_river()
            case Street.RIVER:
                self.table.advance_to_showdown()

    def get_table_info(self):
        """
        Get the table info from the data and set it to the table object
        """
        self.get_hand_id()
        self.get_datetime()

    def reset_table(self):
        """
        Reset the table object
        """
        del self.table
        table = Table()
        self.table = table

    def convert_history(self, file_key: str) -> Table:
        """
        Convert a hand history file into a table object

        Args:
            file_key (str): Path to the hand history file

        Returns:
            (Table): Table object
        """
        print(f"Converting file {file_key}")
        self.reset_table()
        try:
            self.get_parsed_data(file_key)
            self.get_table_info()
            self.get_pregame_info()
            self.get_players()
            self.get_hero()
            self.get_postings()
            self.get_actions()
            self.get_showdown()
            self.get_winners()
            return self.table
        except (HandConversionError, NotSufficientBetError, NotSufficientRaiseError, PlayerNotOnTableError, ValueError,
                KeyError, ShowdownNotReachedError, CannotParseWinnersError, AttributeError):
            raise HandConversionError(file_key)

    def slow_convert_histories(self):
        parsed_keys = self.list_parsed_histories_keys()
        for parsed_key in tqdm(parsed_keys):
            try:
                self.convert_history(parsed_key)
            except HandConversionError:
                self.move_to_correction_dir(parsed_key)

    # def convert_histories(self):
    #     parsed_keys = self.list_parsed_histories_keys()
    #     with ThreadPoolExecutor(max_workers=10) as executor:
    #         futures = [executor.submit(self.convert_history, parsed_key) for parsed_key in parsed_keys]
    #         for future in as_completed(futures):
    #             future.result()
    def convert_histories(self):
        parsed_keys = self.list_parsed_histories_keys()
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(self.convert_history, parsed_key): parsed_key for parsed_key in parsed_keys}
            for future in as_completed(futures):
                parsed_key = futures[future]
                try:
                    future.result()
                except HandConversionError as e:
                    print(f"Error processing history {parsed_key}: {e}")
                    self.move_to_correction_dir(parsed_key)
