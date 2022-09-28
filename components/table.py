from components.board import Board
from components.card import Deck
from components.constants import Street
from components.players import Players
from components.pot import Pot
from components.tournament import Level, Tournament
from components.evaluator import Evaluator


class Table:
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
    evaluator: Evaluator

    def __init__(self):
        self._board = Board()
        self._deck = Deck()
        self._deck.shuffle()
        self._players = Players()
        self._pots = [Pot()]
        self.evaluator = Evaluator()
        self._is_mtt = False
        self._street = Street.PREFLOP

    @property
    def board(self):
        return self._board

    @property
    def deck(self):
        return self._deck

    @property
    def players(self):
        return self._players

    @property
    def current_pot(self):
        return self._pots[len(self._pots)-1]

    @property
    def max_players(self):
        return self._max_players

    @max_players.setter
    def max_players(self, max_value):
        if max_value not in range(1, 11):
            raise ValueError("Number of players should be between 1 and 10")
        else:
            self._max_players = max_value

    @property
    def pot(self) -> float:
        return sum((pot.value for pot in self._pots))

    @property
    def tournament(self):
        return self._tournament

    @tournament.setter
    def tournament(self, tournament):
        self._tournament = tournament

    @property
    def street(self):
        return self._street

    @street.setter
    def street(self, street):
        self._street = Street(street)

    @property
    def level(self):
        if self._is_mtt:
            return self._tournament.level
        else:
            return self._level

    @level.setter
    def level(self, level):
        self._level = level

    @property
    def playing_order(self):
        if self._street == Street.PREFLOP:
            return self.players.preflop_ordered_seats
        else:
            return self.players.postflop_ordered_seats

    @property
    def players_waiting(self):
        return [self.players[i] for i in self.playing_order if self.players[i].can_play]

    @property
    def players_in_game(self):
        return [self.players[i] for i in self.playing_order if self.players[i].in_game]

    @property
    def players_involved(self):
        return [self.players[i] for i in self.playing_order if not self.players[i].folded]

    @property
    def seats_playing(self):
        return [pl.seat for pl in self.players_waiting]

    @property
    def nb_waiting(self):
        return len(self.players_waiting)

    @property
    def nb_involved(self):
        return len(self.players_involved)

    def draw_flop(self, c1=None, c2=None, c3=None):
        if len(self._board) > 0:
            raise ValueError("Board must be empty before we can draw a flop")
        c1 = self._deck.draw(c1)
        c2 = self._deck.draw(c2)
        c3 = self._deck.draw(c3)
        self._board.add(c1)
        self._board.add(c2)
        self._board.add(c3)

    def flop(self, c1=None, c2=None, c3=None):
        self.draw_flop(c1=c1, c2=c2, c3=c3)
        self.street_reset()
        self.street = "flop"

    def draw_turn(self, card=None):
        if len(self._board) != 3:
            raise ValueError("Board size must be 3 before we can draw a turn")
        card = self._deck.draw(card)
        self._board.add(card)

    def turn(self, card=None):
        self.draw_turn(card)
        self.street = "turn"
        self.street_reset()

    def draw_river(self, card=None):
        if len(self._board) != 4:
            raise ValueError("Board size must be 4 before we can draw a turn")
        card = self._deck.draw(card)
        self._board.add(card)

    def river(self, card=None):
        self.draw_river(card)
        self.street = "river"
        self.street_reset()

    def add_tournament(self, tournament):
        self.tournament = tournament
        self._is_mtt = True

    def post_antes(self):
        for i in self.players.preflop_ordered_seats:
            player = self.players.seat_dict[i]
            player.post(self.level.ante)

    def post_sb(self):
        seat = self.players.seats_mapper["SB"]
        player = self.players.seat_dict[seat]
        if player.can_play:
            player.do_bet(self.level.sb)
            player.played = False

    def post_bb(self):
        seat = self.players.seats_mapper["BB"]
        player = self.players.seat_dict[seat]
        if player.can_play:
            player.do_bet(self.level.bb)
            player.played = False

    def post_pregame(self):
        self.post_antes()
        self.post_sb()
        self.post_bb()

    @property
    def seat_playing(self):
        if not hasattr(self, "_seat_playing"):
            self._seat_playing = self.playing_order[0]
        return self._seat_playing

    @property
    def min_bet(self):
        if not hasattr(self, "_min_bet"):
            self._min_bet = self.level.bb*2
        return self._min_bet

    @min_bet.setter
    def min_bet(self, value):
        self._min_bet = value

    def advance_seat_playing(self):
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
        self.current_pot.highest_bet = 0
        self.min_bet = self.level.bb
        for player in self.players_in_game:
            player.reset()

    @property
    def current_player(self):
        return self.players[self.seat_playing]
