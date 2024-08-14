from attrs import define, field, Factory
from attrs.validators import instance_of, optional, ge, le
from datetime import datetime
from pkrcomponents.components.cards.board import Board
from pkrcomponents.components.cards.card import Card
from pkrcomponents.components.cards.combo import Combo
from pkrcomponents.components.cards.deck import Deck
from pkrcomponents.components.cards.flop import Flop
from pkrcomponents.components.actions.street import Street
from pkrcomponents.components.players.players import Players
from pkrcomponents.components.tables.pot import Pot
from pkrcomponents.components.tournaments.tournament import Level, Tournament
from pkrcomponents.components.cards.evaluator import Evaluator
from pkrcomponents.components.utils.converters import convert_to_street
from pkrcomponents.components.utils.exceptions import CannotParseWinnersError


@define(repr=False)
class Table:
    """
    This class represents a poker table

    Attributes:
        board(Board): The board of the table
        cnt_bets(int): The number of bets made on the table at a given street
        cnt_calls(int): The number of calls made on the table at a given street
        cnt_cold_calls(int): The number of cold calls made on the table at a given street
        cnt_limps (int): The number of limps made on the table at preflop
        deck(Deck): The deck of the table
        evaluator(Evaluator): The evaluator of the table
        hand_has_started(bool): Whether the hand has started
        hand_id(str): The ID of the hand
        hand_date(datetime): The date of the hand
        hero_combo(Combo): The combo of the hero
        is_mtt(bool): Whether the table is a tournament
        is_opened(bool): Whether the table is opened
        level(Level): The level of the table
        max_players(int): The maximum number of players on the table
        min_bet(float): The minimum bet on the table
        players(Players): The players on the table
        pot(Pot): The pot of the table
        rewards_table (list): The rewards table
        seat_playing(int): The seat of the player currently playing
        street(Street): The current street of the table
        tournament(Tournament): The tournament associated with the table

    Methods:


    """
    preflop_bet_factors = [1, 1.1, 1.25, 1.5, 2, 3.5, 5]
    postflop_bet_factors = [
        {"text": "1/4 Pot", "value": 1 / 4},
        {"text": "1/3 Pot", "value": 1 / 3},
        {"text": "1/2 Pot", "value": 1 / 2},
        {"text": "2/3 Pot", "value": 2 / 3},
        {"text": "3/4 Pot", "value": 3 / 4},
        {"text": "Pot", "value": 1}
    ]

    board = field(default=Factory(Board), validator=instance_of(Board))
    cnt_bets = field(default=0, validator=[instance_of(int), ge(0)])
    cnt_calls = field(default=0, validator=[instance_of(int), ge(0)])
    cnt_cold_calls = field(default=0, validator=[instance_of(int), ge(0)])
    cnt_limps = field(default=0, validator=[instance_of(int), ge(0)])
    deck = field(default=Factory(Deck), validator=instance_of(Deck))
    evaluator = field(default=Factory(Evaluator), validator=instance_of(Evaluator))
    hand_has_started = field(default=False, validator=instance_of(bool))
    hand_id = field(default=None, validator=optional(instance_of(str)))
    hero_combo = field(default=None, validator=optional(instance_of(Combo)))
    is_mtt = field(default=False, validator=instance_of(bool))
    is_opened = field(default=False, validator=instance_of(bool))
    level = field(default=Factory(Level), validator=instance_of(Level))
    max_players = field(default=6, validator=[instance_of(int), ge(2), le(10)])
    min_bet = field(default=0, validator=[instance_of(float), ge(0)], converter=float)
    players = field(default=Factory(Players), validator=instance_of(Players))
    postings = field(default=[], validator=instance_of(list))
    pot = field(default=Factory(Pot), validator=instance_of(Pot))
    seat_playing = field(default=0, validator=[instance_of(int), ge(0)])
    hand_date = field(default=None, validator=optional(instance_of(datetime)))
    street = field(default=None, validator=optional(instance_of(Street)), converter=convert_to_street)
    tournament = field(default=None, validator=optional(instance_of(Tournament)))
    total_buy_in = field(default=0, validator=[instance_of(float), ge(0)], converter=float)
    rewards_table = field(default=[], validator=instance_of(list))

    def __attrs_post_init__(self):
        self.deck.shuffle()
        self.postings = list()
        self.rewards_table = list()

    def __repr__(self):
        return f"Table(max_players={self.max_players}), Tournament={self.tournament})"

    @property
    def cnt_players(self) -> int:
        """Returns the number of players on the table"""
        return self.players.len

    @property
    def is_full(self) -> bool:
        """Returns True if the table is full"""
        return self.cnt_players == self.max_players

    @property
    def is_empty(self) -> bool:
        """Returns True if the table is empty"""
        return self.cnt_players == 0

    @property
    def bb_forced_into_all_in(self) -> bool:
        """Returns True if the big blind was forced into all-in"""
        bb_seat = self.players.bb_seat
        bb_player = self.players[bb_seat]
        return (bb_player.current_bet < self.level.bb and self.cnt_bets == 1 and self.street == Street.PREFLOP
                and self.cnt_calls == 0)

    @property
    def playing_order(self) -> list[int]:
        """Returns the list of the indexes of players on the table, with order depending on current street"""
        if self.street.is_preflop:
            return self.players.preflop_ordered_seats
        else:
            return self.players.postflop_ordered_seats

    @property
    def players_order(self) -> list:
        """Returns the players in playing order"""
        return [self.players[i] for i in self.playing_order]

    @property
    def players_able_to_play(self) -> list:
        """Returns the list of players on the table that are able to play"""
        return [player for player in self.players_order if player.can_play]

    @property
    def players_waiting(self) -> list:
        """Returns the list of players on the table that are waiting"""
        return [player for player in self.players_order if player.is_waiting]

    @property
    def street_ended(self) -> bool:
        """Returns True if the street has ended"""
        return not self.has_players_waiting or self.one_player_left or self.showdown_is_over

    @property
    def players_in_game(self) -> list:
        """Returns the list of players on the table that are still in the game (they can make an action)"""
        return [player for player in self.players_order if player.in_game]

    @property
    def players_involved(self) -> list:
        """Returns the list of players on the table that didn't fold yet"""
        return [player for player in self.players_order if not player.folded]

    @property
    def hand_ended(self) -> bool:
        """Returns True if the hand has ended"""
        return self.nb_involved == 1 or self.is_at_showdown

    @property
    def next_street_ready(self) -> bool:
        """Returns True if the next street is ready to be played"""
        return self.street_ended and not self.hand_ended

    @property
    def next_hand_ready(self) -> bool:
        """Returns True if the next hand is ready to be played"""
        return self.hand_ended and self.street_ended

    @property
    def seats_playing(self) -> list[int]:
        """Returns the list of seats of players waiting to play"""
        return [pl.seat for pl in self.players_able_to_play]

    @property
    def nb_able_to_play(self) -> int:
        """Returns the number of players that are able to play"""
        return len(self.players_able_to_play)

    @property
    def nb_waiting(self) -> int:
        """Returns the number of players that are waiting to play in this street"""
        return len(self.players_waiting)

    @property
    def has_players_able_to_play(self):
        """Returns True if there are players waiting to play"""
        return self.nb_able_to_play > 0

    @property
    def has_players_waiting(self):
        """Returns True if there are players waiting to play"""
        return self.nb_waiting > 0

    @property
    def nb_in_game(self) -> int:
        """Returns the number of players still in the game"""
        return len(self.players_in_game)

    @property
    def nb_involved(self) -> int:
        """Returns the number of players who didn't fold yet"""
        return len(self.players_involved)

    @property
    def one_player_left(self) -> bool:
        """Returns True if there is only one player left in the game that can play and he has called"""
        return (self.nb_able_to_play == 1 and self.nb_in_game == 1 and self.players_able_to_play[0].is_biggest_investor
                and not self.is_at_showdown)

    @property
    def hand_can_start(self) -> bool:
        """Returns True if the hand can start"""
        return self.cnt_players >= 2 and not self.hand_has_started

    def set_starting_status(self):
        """Set the starting status of the table"""
        self.hand_has_started = True
        self.street = Street.PREFLOP
        self.is_opened = False
        self.street_reset()
        for player in self.players:
            player.hand_stats.general.starting_stack = player.init_stack

    def start_hand(self):
        """Starts a new hand"""
        self.set_starting_status()
        self.post_pregame()

    def draw_flop(self, card1: (str, Card) = None, card2: (str, Card) = None, card3: (str, Card) = None):
        """
        For the flop, draws 3 cards in the deck and adds them on the board as flop cards

        Args:
            card1 (str, Card): The first card to draw
            card2 (str, Card): The second card to draw
            card3 (str, Card): The third card to draw
        """
        if len(self.board) > 0:
            raise ValueError("Board must be empty before we can draw a flop")
        card1 = self.deck.draw(card1)
        card2 = self.deck.draw(card2)
        card3 = self.deck.draw(card3)
        flop = Flop(card1, card2, card3)
        self.board.add(flop.first_card)
        self.board.add(flop.second_card)
        self.board.add(flop.third_card)

    def execute_flop(self, card1: (str, Card) = None, card2: (str, Card) = None, card3: (str, Card) = None):
        """
        Draw a flop and steps to this new street

        Args:
            card1 (str, Card): The first card to draw
            card2 (str, Card): The second card to draw
            card3 (str, Card): The third card to draw
        """
        if not (self.next_street_ready and self.street == Street.PREFLOP):
            raise ValueError("The PREFLOP must be ended before we can draw a flop")
        self.draw_flop(card1=card1, card2=card2, card3=card3)
        self.street = Street.FLOP
        self.street_reset()

    def draw_turn(self, card: (str, Card) = None):
        """
        For the turn, draws a card in the deck and adds it on the board as turn card

        Args:
            card (str, Card): The card to draw
        """
        if len(self.board) != 3:
            raise ValueError("Board size must be 3 before we can draw a turn")
        card = self.deck.draw(card)
        self.board.add(card)

    def execute_turn(self, card: (str, Card) = None):
        """
        Draw a turn and steps to this new street

        Args:
            card (str, Card): The card to draw
        """
        if not (self.next_street_ready and self.street == Street.FLOP):
            raise ValueError("The FLOP must be ended before we can draw a turn")
        self.draw_turn(card)
        self.street = Street.TURN
        self.street_reset()

    def draw_river(self, card: (str, Card) = None):
        """
        For the river, draws a card in the deck and adds it on the board as river card

        Args:
            card (str, Card): The card to draw
        """
        if len(self.board) != 4:
            raise ValueError("Board size must be 4 before we can draw a turn")
        card = self.deck.draw(card)
        self.board.add(card)

    def execute_river(self, card: (str, Card) = None):
        """
        Draw a river and steps to this new street

        Args:
            card (str, Card): The card to draw
        """
        if not (self.next_street_ready and self.street == Street.TURN):
            raise ValueError("The TURN must be ended before we can draw a river")
        self.draw_river(card)
        self.street = Street.RIVER
        self.street_reset()

    def advance_to_showdown(self):
        """Advance to showdown"""
        if not (self.next_street_ready and self.street == Street.RIVER):
            raise ValueError("The RIVER must be ended before we can advance to showdown")
        self.street = Street.SHOWDOWN
        self.street_reset()

    def add_tournament(self, tournament: Tournament):
        """
        Associates table with a tournament

        Args:
            tournament (Tournament): The tournament to associate with the table
        """
        self.tournament = tournament
        if self.tournament.has_level:
            self.set_level(tournament.level)
        else:
            self.tournament.set_level(self.level)
        self.set_total_buy_in(tournament.buy_in.total)
        self.is_mtt = True

    def add_player(self, player):
        """
        Add a player to the table

        Args:
            player (TablePlayer): The player to add
        """
        player.sit(self)
        if self.cnt_players > 1:
            self.players.distribute_positions()
        else:
            self.players.bb = player.seat

    def remove_player(self, player):
        """
        Remove a player from the table

        Args:
            player (TablePlayer): The player to remove
        """
        player.sit_out()
        if self.cnt_players > 1:
            self.players.distribute_positions()

    def set_hero(self, player):
        """
        Set a player as the hero

        Args:
            player (TablePlayer): The player to set as the hero
        """
        for p in self.players:
            p.is_hero = False
        player.is_hero = True
        player.hand_stats.general.flag_is_hero = True

    def set_level(self, level: Level):
        """
        Set the level of the table

        Args:
            level (Level): The level to set
        """
        self.level = level

    def set_total_buy_in(self, total_buy_in: float):
        """
        Set the total buy-in for the table

        Args:
            total_buy_in (float): The total buy-in
        """
        self.total_buy_in = total_buy_in

    def distribute_hero_cards(self, player_name: str, card1: (str, Card), card2: (str, Card)):
        """
        Distribute hero cards

        Args:
            player_name (str): The name of the player
            card1 (str, Card): The first card
            card2 (str, Card): The second card
        """
        player = self.players[player_name]
        self.set_hero(player)
        player.distribute(f"{card1}{card2}")
        self.hero_combo = player.combo

    def set_bb_seat(self, player_seat: int):
        """
        Set the seat of the big blind player and redistribute positions

        Args:
            player_seat (int): The seat of the big blind player
        """
        self.players.bb_seat = player_seat
        if self.cnt_players > 1:
            self.players.distribute_positions()

    def advance_bb_seat(self):
        """Advances the Big Blind seat"""
        self.players.advance_bb_seat()

    def set_max_players(self, max_players: int):
        """
        Set the maximum number of players on the table

        Args:
            max_players (int): The maximum number of players on the table
        """
        self.max_players = max_players
        if self.cnt_players > 1:
            self.players.distribute_positions()

    def post_pregame(self):
        """Preflop posting antes and blinds"""
        self.players.post_antes()
        self.players.post_sb()
        self.players.post_bb()

    @property
    def cost_per_round(self) -> float:
        """Returns the cost of a round for a player"""
        return self.level.bb * 1.5 + self.level.ante * self.cnt_players

    @property
    def min_bet_bb(self) -> float:
        """Returns the minimum bet in big blinds"""
        return self.min_bet/self.level.bb

    @property
    def pot_value(self) -> float:
        """Returns the pot's value"""
        return self.pot.value

    @property
    def pot_value_bb(self) -> float:
        """Returns the pot's value in big blinds"""
        return round(self.pot_value/self.level.bb, 2)

    @property
    def average_stack(self) -> float:
        """Returns the average stack of players on the table"""
        return sum(pl.init_stack for pl in self.players) / self.cnt_players

    @property
    def average_stack_bb(self) -> float:
        """Returns the average stack in big blinds"""
        return round(self.average_stack/self.level.bb, 2)

    @property
    def estimated_players_remaining(self) -> int:
        """Returns the estimated number of players remaining in the tournament"""
        return self.tournament.estimated_players_remaining(average_stack=self.average_stack)

    def advance_seat_playing(self):
        """Advances seat playing to next available player"""
        self.seat_playing = self.next_seat
        if not self.current_player.can_play and self.has_players_able_to_play:
            self.advance_seat_playing()

    @property
    def next_player(self):
        """ Returns the next player after the current player"""
        current_player_index = self.players_order.index(self.current_player)
        next_index = current_player_index + 1 if current_player_index < len(self.players_order) - 1 else 0
        return self.players_order[next_index]

    @property
    def next_seat(self) -> int:
        """ Returns the next seat to play after the current player"""
        return self.next_player.seat

    def update_min_bet(self, value):
        """Update the minimum bet on the table"""
        self.min_bet = value

    def street_reset(self):
        """Reset status of players in game and betting status for a new street"""
        self.pot.highest_bet = 0
        self.cnt_bets = 0
        self.cnt_calls = 0
        self.cnt_cold_calls = 0
        self.update_min_bet(self.level.bb)
        try:
            self.seat_playing = self.players_in_game[0].seat
            for player in self.players_in_game:
                player.reset_street_status()
                player.update_has_position_stat()

        except IndexError:
            # raise IndexError
            pass

    @property
    def current_player(self):
        """Returns the player currently playing"""
        return self.players[self.seat_playing]

    @property
    def unrevealed_players(self) -> list:
        """Returns the list of players that have not revealed their cards"""
        return [pl for pl in self.players_involved if not pl.has_combo]

    @property
    def nb_unrevealed(self) -> int:
        """Returns the number of players that have not revealed their cards"""
        return len(self.unrevealed_players)

    @property
    def has_unrevealed_players(self) -> bool:
        """Returns True if there are players that have not revealed their cards"""
        return self.nb_unrevealed > 0

    @property
    def is_at_showdown(self):
        """Returns True if the table is at showdown"""
        return self.street == Street.SHOWDOWN

    @property
    def showdown_is_over(self) -> bool:
        """Returns True if the showdown is over"""
        return self.is_at_showdown and not self.has_unrevealed_players

    @property
    def can_parse_winners(self) -> bool:
        """Returns True if the winners can be parsed"""
        return self.hand_ended and self.nb_unrevealed == 0 or self.nb_involved == 1


    def get_winners(self) -> dict[int, list]:
        """Current status of winners with associated scores"""
        if not self.can_parse_winners:
            raise CannotParseWinnersError
        elif self.nb_involved == 1:
            return {1: [self.players_involved[0]]}
        else:
            winners = {}
            for player in self.players_involved:
                pl_score = player.hand_score
                if not winners.get(pl_score):
                    winners[pl_score] = [player]
                else:
                    winners[pl_score].append(player)
            return winners

    def split_pot(self, winning_players: list):
        """
        Split pot between players

        Args:
            winning_players (list): The list of players to split the pot between
        """
        winning_players_copy = winning_players.copy()
        while len(winning_players_copy) > 0 and self.pot.value > 0:
            remaining_players_minimum_reward = min([player.max_reward for player in winning_players_copy])
            max_reward_from_pot = self.pot.value/len(winning_players_copy)
            reward_given_to_each_player = min(remaining_players_minimum_reward, max_reward_from_pot)
            for player in winning_players_copy:
                player.hand_reward += reward_given_to_each_player
                if player.hand_reward >= player.max_reward or player.hand_reward >= self.pot.value:
                    reward_dict = {"player": player, "reward": player.hand_reward}
                    winning_players_copy.remove(player)
                    self.rewards_table.append(reward_dict)
                    self.pot.value -= reward_given_to_each_player

    def calculate_rewards(self):
        """
        Calculate rewards for each player
        """
        winners = self.get_winners()
        scores = [score for score in winners.keys()]
        scores.sort()
        for score in scores:
            winning_players = winners[score]
            self.split_pot(winning_players)

    def distribute_rewards(self):
        """Distribute rewards between players"""
        hand_winner = self.rewards_table[0]["player"]
        hand_winner.hand_stats.general.flag_won_hand = True
        for reward_dict in self.rewards_table:
            player = reward_dict["player"]
            reward = reward_dict["reward"]
            player.win(reward)

    def calculate_and_distribute_rewards(self):
        """Calculate and distribute rewards"""
        self.calculate_rewards()
        self.distribute_rewards()

    def hand_reset(self):
        """Reset the table for a new hand"""
        self.street = Street.PREFLOP
        self.pot.reset()
        self.deck.reset()
        self.board.reset()
        self.players.hand_reset()
        self.reset_postings()
        self.hand_has_started = False
        self.rewards_table = []

    def advance_to_next_hand(self):
        """Advance to the next hand"""
        self.hand_reset()
        self.players.advance_bb_seat()

    def reset_postings(self):
        """Reset the postings"""
        self.postings = list()
