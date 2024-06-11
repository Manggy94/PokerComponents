from attrs import define, field, Factory
from attrs.validators import instance_of, optional, ge, gt, le
from datetime import datetime
from pkrcomponents.board import Board
from pkrcomponents.card import Card
from pkrcomponents.deck import Deck
from pkrcomponents.constants import Street
from pkrcomponents.players import Players
from pkrcomponents.pot import Pot
from pkrcomponents.tournament import Level, Tournament
from pkrcomponents.evaluator import Evaluator
from pkrcomponents.utils.converters import convert_to_street


@define
class Table:
    """
    This class represents a poker table

    Attributes:
        board(Board): The board of the table
        cnt_bets(int): The number of bets made on the table
        deck(Deck): The deck of the table
        evaluator(Evaluator): The evaluator of the table
        hand_has_started(bool): Whether the hand has started
        hand_id(str): The ID of the hand
        is_mtt(bool): Whether the table is a tournament
        level(Level): The level of the table
        max_players(int): The maximum number of players on the table
        min_bet(float): The minimum bet on the table
        players(Players): The players on the table
        pot(Pot): The pot of the table
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
    deck = field(default=Factory(Deck), validator=instance_of(Deck))
    evaluator = field(default=Factory(Evaluator), validator=instance_of(Evaluator))
    hand_has_started = field(default=False, validator=instance_of(bool))
    hand_id = field(default=None, validator=optional(instance_of(str)))
    is_mtt = field(default=False, validator=instance_of(bool))
    level = field(default=Factory(Level), validator=instance_of(Level))
    max_players = field(default=6, validator=[instance_of(int), gt(2), le(10)])
    min_bet = field(default=0, validator=[instance_of(float), ge(0)], converter=float)
    players = field(default=Factory(Players), validator=instance_of(Players))
    pot = field(default=Factory(Pot), validator=instance_of(Pot))
    seat_playing = field(default=0, validator=[instance_of(int), ge(0)])
    start_date = field(default=None, validator=optional(instance_of(datetime)))
    street = field(default=None, validator=optional(instance_of(Street)), converter=convert_to_street)
    tournament = field(default=None, validator=optional(instance_of(Tournament)))

    def __attrs_post_init__(self):
        self.deck.shuffle()

    def __repr__(self):
        return f"Table(max_players={self.max_players}), Tournament={self.tournament})"

    @property
    def is_full(self) -> bool:
        """Returns True if the table is full"""
        return self.players.len == self.max_players

    @property
    def is_empty(self) -> bool:
        """Returns True if the table is empty"""
        return self.players.len == 0

    @property
    def playing_order(self) -> list[int]:
        """Returns the list of the indexes of players on the table, with order depending on current street"""
        if self.street == Street.PREFLOP:
            return self.players.preflop_ordered_seats
        else:
            return self.players.postflop_ordered_seats

    @property
    def players_order(self) -> list:
        """Returns the players in playing order"""
        return [self.players[i] for i in self.playing_order]

    @property
    def players_waiting(self) -> list:
        """Returns the list of players on the table that are waiting to play"""
        return [player for player in self.players_order if player.can_play]

    @property
    def street_ended(self) -> bool:
        """Returns True if the street has ended"""
        return len(self.players_waiting) == 0 or (
                self.nb_waiting == 1
                and self.nb_in_game == 1
                and self.players_waiting[0].to_call == 0
                and self.street != Street.SHOWDOWN) or (
                self.street == Street.SHOWDOWN and len(self.unrevealed_players) == 0
        )

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
        return self.nb_involved == 1 or self.street == Street.SHOWDOWN

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
        return [pl.seat for pl in self.players_waiting]

    @property
    def nb_waiting(self) -> int:
        """Returns the number of players waiting to play"""
        return len(self.players_waiting)

    @property
    def nb_in_game(self) -> int:
        """Returns the number of players still in the game"""
        return len(self.players_in_game)

    @property
    def nb_involved(self) -> int:
        """Returns the number of players who didn't fold yet"""
        return len(self.players_involved)

    @property
    def hand_can_start(self) -> bool:
        """Returns True if the hand can start"""
        return self.players.len >= 2 and not self.hand_has_started

    def start_hand(self):
        """Starts a new hand"""
        self.hand_has_started = True
        self.street = Street.PREFLOP
        self.street_reset()
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
        self.board.add(card1)
        self.board.add(card2)
        self.board.add(card3)

    def flop(self, card1: (str, Card) = None, card2: (str, Card) = None, card3: (str, Card) = None):
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
        self.street = "flop"
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

    def turn(self, card: (str, Card) = None):
        """
        Draw a turn and steps to this new street

        Args:
            card (str, Card): The card to draw
        """
        if not (self.next_street_ready and self.street == Street.FLOP):
            raise ValueError("The FLOP must be ended before we can draw a turn")
        self.draw_turn(card)
        self.street = "turn"
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

    def river(self, card: (str, Card) = None):
        """
        Draw a river and steps to this new street

        Args:
            card (str, Card): The card to draw
        """
        if not (self.next_street_ready and self.street == Street.TURN):
            raise ValueError("The TURN must be ended before we can draw a river")
        self.draw_river(card)
        self.street = "river"
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
        self.level = tournament.level
        self.is_mtt = True

    def add_player(self, player):
        """
        Add a player to the table

        Args:
            player (TablePlayer): The player to add
        """
        player.sit(self)
        if self.players.len > 1:
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
        if self.players.len > 1:
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

    def set_bb_seat(self, player_seat: int):
        """
        Set the seat of the big blind player and redistribute positions

        Args:
            player_seat (int): The seat of the big blind player
        """
        self.players.bb = player_seat
        if self.players.len > 1:
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
        if self.players.len > 1:
            self.players.distribute_positions()

    def post_antes(self):
        """Preflop Ante posting for players on the table"""
        for i in self.players.preflop_ordered_seats:
            player = self.players.seat_dict[i]
            player.post(self.level.ante)

    def post_sb(self):
        """Preflop small blind posting"""
        seat = self.players.seats_mapper["SB"]
        player = self.players.seat_dict[seat]
        if player.can_play:
            player.do_bet(self.level.sb)
            player.played = False

    def post_bb(self):
        """Preflop big blind posting"""
        seat = self.players.seats_mapper["BB"]
        player = self.players.seat_dict[seat]
        if player.can_play:
            player.do_bet(self.level.bb)
            player.played = False
        self.min_bet = self.level.bb*2

    def post_pregame(self):
        """Preflop posting antes and blinds"""
        self.post_antes()
        self.post_sb()
        self.post_bb()

    @property
    def cost_per_round(self) -> float:
        """Returns the cost of a round for a player"""
        return self.level.bb * 1.5 + self.level.ante * self.players.len

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
        return sum(pl.init_stack for pl in self.players) / self.players.len

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
        if not self.current_player.can_play and self.nb_waiting > 0:
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

    def street_reset(self):
        """Reset status of players in game and betting status for a new street"""
        self.pot.highest_bet = 0
        self.cnt_bets = 0
        self.min_bet = self.level.bb
        self.seat_playing = self.players_in_game[0].seat
        for player in self.players_in_game:
            player.reset_street_status()

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
    def can_parse_winners(self) -> bool:
        """Returns True if the winners can be parsed"""
        return self.hand_ended and self.nb_unrevealed == 0 or self.nb_involved == 1

    @property
    def winners(self) -> dict[int, list]:
        """Current status of winners with associated scores"""
        if not self.can_parse_winners:
            raise ValueError("Winners can't be parsed yet")
        if self.nb_involved == 1:
            return {1: [self.players_involved[0]]}
        winners = {}
        for player in self.players_involved:
            pl_score = player.hand_score
            if not winners.get(pl_score):
                winners[pl_score] = [player]
            else:
                winners[pl_score].append(player)
        return winners

    def split_pot(self, players: list):
        """
        Split pot between players

        Args:
            players (list): The list of players to split the pot between
        """
        while len(players) > 0 and self.pot.value > 0:
            min_reward = min([pl.max_reward for pl in players])
            reward = min(min_reward, self.pot.value/len(players))
            for player in players:
                player.reward += reward
                if player.reward >= player.max_reward:
                    players.remove(player)
                    player.win(reward)

    def distribute_rewards(self):
        """Distribute rewards between players"""
        scores = [score for score in self.winners.keys()]
        scores.sort()
        for score in scores:
            players = self.winners[score]
            self.split_pot(players)

    def hand_reset(self):
        """Reset the table for a new hand"""
        self.street = Street.PREFLOP
        self.pot.reset()
        self.deck.reset()
        self.board.reset()
        self.players.hand_reset()
        self.hand_has_started = False

    def advance_to_next_hand(self):
        """Advance to the next hand"""
        self.hand_reset()
        self.players.advance_bb_seat()
