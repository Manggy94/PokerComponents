from functools import cached_property
from pkrcomponents.board import Board
from pkrcomponents.card import Deck
from pkrcomponents.constants import Street
from pkrcomponents.players import Players
from pkrcomponents.pot import Pot
from pkrcomponents.tournament import Level, Tournament
from pkrcomponents.evaluator import Evaluator


class Table:
    """Class representing a poker table"""
    _ident: str
    _board: Board
    _deck: Deck
    _players: Players
    _pots: [Pot]
    _max_players: int
    _is_mtt: bool
    _tournament: Tournament
    _level: Level
    _street: Street
    _seat_playing: int
    _min_bet: float
    _cnt_bets: int
    _evaluator: Evaluator
    _preflop_bet_factors = [1, 1.1, 1.25, 1.5, 2, 3.5, 5]
    _postflop_bet_factors = [
        {"text": "1/4 Pot", "value": 1 / 4},
        {"text": "1/3 Pot", "value": 1 / 3},
        {"text": "1/2 Pot", "value": 1 / 2},
        {"text": "2/3 Pot", "value": 2 / 3},
        {"text": "3/4 Pot", "value": 3 / 4},
        {"text": "Pot", "value": 1}
    ]

    def __init__(self, max_players=6):
        self._board = Board()
        self._deck = Deck()
        self._deck.shuffle()
        self._players = Players()
        self._pot = Pot()
        self._evaluator = Evaluator()
        self._is_mtt = False
        self._street = Street.PREFLOP
        self.max_players = max_players
        self._hand_has_started = False
        self._cnt_bets = 0

    @property
    def board(self) -> Board:
        """Returns the associated board """
        return self._board

    @property
    def deck(self) -> Deck:
        """Returns the associated deck """
        return self._deck

    @property
    def players(self) -> Players:
        """Returns the associated players """
        return self._players

    @property
    def max_players(self) -> int:
        """Returns the maximum players that can be added on this table"""
        return self._max_players

    @max_players.setter
    def max_players(self, max_value):
        """Setter for max players property"""
        if max_value not in range(1, 11):
            raise ValueError("Number of players should be between 1 and 10")
        else:
            self._max_players = max_value

    @property
    def is_full(self) -> bool:
        """Returns True if the table is full"""
        return self.players.len == self.max_players

    @property
    def is_empty(self) -> bool:
        """Returns True if the table is empty"""
        return self.players.len == 0

    @property
    def pot(self):
        """Returns the associated pot """
        return self._pot

    @property
    def tournament(self) -> Tournament or None:
        """Returns the associated tournament """
        return self._tournament

    @property
    def evaluator(self) -> Evaluator:
        """Returns the associated evaluator"""
        return self._evaluator

    @tournament.setter
    def tournament(self, tournament):
        """Setter for tournament property"""
        self._tournament = tournament

    @property
    def street(self) -> Street:
        """Returns table's current street"""
        return self._street

    @street.setter
    def street(self, street):
        """Setter for street property"""
        self._street = Street(street)

    @property
    def level(self) -> Level:
        """Returns current level"""
        if self._is_mtt:
            return self._tournament.level
        else:
            return self._level

    @level.setter
    def level(self, level):
        """Setter for level property"""
        self._level = level

    @property
    def playing_order(self) -> list[int]:
        """Returns the list of the indexes of players on the table, with order depending on current street"""
        if self._street == Street.PREFLOP:
            return self.players.preflop_ordered_seats
        else:
            return self.players.postflop_ordered_seats

    @property
    def players_waiting(self) -> list:
        """Returns the list of players on the table that are waiting to play"""
        return [self.players[i] for i in self.playing_order if self.players[i].can_play]

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
        return [self.players[i] for i in self.playing_order if self.players[i].in_game]

    @property
    def players_involved(self) -> list:
        """Returns the list of players on the table that didn't fold yet"""
        return [self.players[i] for i in self.playing_order if not self.players[i].folded]

    @property
    def hand_ended(self) -> bool:
        """Returns True if the hand has ended"""
        return len(self.players_involved) == 1 or self.street == Street.SHOWDOWN

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
    def hand_has_started(self) -> bool:
        """Returns True if the hand has started"""
        return self._hand_has_started

    @property
    def hand_can_start(self) -> bool:
        """Returns True if the hand can start"""
        return self.players.len >= 2 and not self.hand_has_started

    def start_hand(self):
        """Starts a new hand"""
        self._hand_has_started = True
        self.street = Street.PREFLOP
        self.street_reset()
        self.post_pregame()

    def draw_flop(self, c1=None, c2=None, c3=None):
        """For the flop, draws 3 cards in the deck and adds them on the board as flop cards"""
        if len(self._board) > 0:
            raise ValueError("Board must be empty before we can draw a flop")
        c1 = self._deck.draw(c1)
        c2 = self._deck.draw(c2)
        c3 = self._deck.draw(c3)
        self._board.add(c1)
        self._board.add(c2)
        self._board.add(c3)

    def flop(self, c1=None, c2=None, c3=None):
        """Draw a flop and steps to this new street"""
        self.draw_flop(c1=c1, c2=c2, c3=c3)
        self.street = "flop"
        self.street_reset()

    def draw_turn(self, card=None):
        """For the turn, draws a card in the deck and adds it on the board as turn card"""
        if len(self._board) != 3:
            raise ValueError("Board size must be 3 before we can draw a turn")
        card = self._deck.draw(card)
        self._board.add(card)

    def turn(self, card=None):
        """Draw a turn and steps to this new street"""
        self.draw_turn(card)
        self.street = "turn"
        self.street_reset()

    def draw_river(self, card=None):
        """For the river, draws a card in the deck and adds it on the board as river card"""
        if len(self._board) != 4:
            raise ValueError("Board size must be 4 before we can draw a turn")
        card = self._deck.draw(card)
        self._board.add(card)

    def river(self, card=None):
        """Draw a river and steps to this new street"""
        self.draw_river(card)
        self.street = "river"
        self.street_reset()

    def advance_to_showdown(self):
        """Advance to showdown"""
        self.street = Street.SHOWDOWN
        self.street_reset()

    def add_tournament(self, tournament):
        """Associates table with a tournament"""
        self.tournament = tournament
        self._is_mtt = True

    def add_player(self, player):
        """
        Add a player to the table
        """
        player.sit(self)
        if self.players.len > 1:
            self.players.distribute_positions()
        else:
            self.players.bb = player.seat

    def remove_player(self, player):
        """
        Remove a player from the table
        """
        player.sit_out()
        if self.players.len > 1:
            self.players.distribute_positions()

    def set_hero(self, player):
        """
        Set a player as the hero
        """
        for p in self.players:
            p.is_hero = False
        player.is_hero = True

    def set_bb_seat(self, player_seat: int):
        """
        Set the seat of the big blind player and redistribute positions
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
    def seat_playing(self):
        """Returns the seat of the player currently playing"""
        if not hasattr(self, "_seat_playing"):
            self._seat_playing = self.playing_order[0]
        return self._seat_playing

    @property
    def cost_per_round(self):
        """Returns the cost of a round for a player"""
        return self.level.bb * 1.5 + self.level.ante * self.players.len

    @property
    def min_bet(self):
        """Returns table current minimum bet a player can make"""
        if not hasattr(self, "_min_bet"):
            self._min_bet = self.level.bb*2
        return self._min_bet

    @min_bet.setter
    def min_bet(self, value: float):
        """Setter for min bet property"""
        if value > self.min_bet:
            self._min_bet = value

    @property
    def min_bet_bb(self):
        """Returns the minimum bet in big blinds"""
        return self.min_bet/self.level.bb

    @property
    def pot_value(self):
        """Returns the pot's value"""
        return self.pot.value

    @property
    def pot_value_bb(self):
        """Returns the pot's value in big blinds"""
        return self.pot_value/self.level.bb

    @property
    def average_stack(self):
        """Returns the average stack of players on the table"""
        return sum(pl.init_stack for pl in self.players) / self.players.len

    @property
    def average_stack_bb(self):
        """Returns the average stack in big blinds"""
        return round(self.average_stack/self.level.bb, 2)

    def estimated_players_remaining(self):
        """Returns the estimated number of players remaining in the tournament"""
        return self.tournament.estimated_players_remaining(average_stack=self.average_stack)

    def advance_seat_playing(self):
        """Advances seat playing to next available player"""
        player = self.current_player
        while not player.can_play and self.nb_waiting > 0:
            idx = self.playing_order.index(player.seat) + 1
            try:
                new_seat = self.playing_order[idx]
            except IndexError:
                new_seat = self.playing_order[0]
            player = self.players[new_seat]
        self._seat_playing = player.seat

    def street_reset(self):
        """Reset status of players in game and betting status for a new street"""
        self.pot.highest_bet = 0
        self.cnt_bets = 0
        self._min_bet = self.level.bb
        self._seat_playing = self.players_in_game[0].seat
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
    def can_parse_winners(self) -> bool:
        """Returns True if the winners can be parsed"""
        return self.hand_ended and len(self.unrevealed_players) == 0

    @property
    def winners(self) -> dict[int, list]:
        """Current status of winners with associated scores"""
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

    def split_pot(self, players):
        """Split pot between players"""
        while len(players) > 0 and self.pot.value > 0:
            min_reward = min([pl.max_reward for pl in players])
            reward = min(min_reward, self.pot.value/len(players))
            for player in players:
                if not hasattr(player, "reward"):
                    player.reward = 0
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

    @property
    def cnt_bets(self) -> int:
        """Returns the number of bets made on the table"""
        return self._cnt_bets

    @cnt_bets.setter
    def cnt_bets(self, value):
        """Setter for cnt bets property"""
        self._cnt_bets = value

    @property
    def preflop_bet_factors(self) -> list:
        """Returns the preflop bet factors"""
        return self._preflop_bet_factors

    @property
    def postflop_bet_factors(self) -> list:
        """Returns the postflop bet factors"""
        return self._postflop_bet_factors

    def hand_reset(self):
        """
        Reset the hand
        """
        self.street = Street.PREFLOP
        self.pot.reset()
        self.deck.reset()
        self.board.reset()
        self.players.hand_reset()
        self._hand_has_started = False

    def advance_to_next_hand(self):
        """Advance to the next hand"""
        self.hand_reset()
        self.players.advance_bb_seat()
