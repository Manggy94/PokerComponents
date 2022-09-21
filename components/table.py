from components.board import Board
from components.card import Deck
from components.players import Players
from components.pot import Pot


class Table:
    _ident: str
    _board: Board
    _deck: Deck
    _players: Players
    _pots: [Pot]
    _max_players: int

    def __init__(self):
        self._board = Board()
        self._deck = Deck()
        self._deck.shuffle()
        self._players = Players()
        self._pots = [Pot()]

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
    def pot(self):
        return sum((pot.value for pot in self._pots))

    def draw_flop(self, c1=None, c2=None, c3=None):
        if len(self._board) > 0:
            raise ValueError("Board must be empty before we can draw a flop")
        c1 = self._deck.draw(c1)
        c2 = self._deck.draw(c2)
        c3 = self._deck.draw(c3)
        self._board.add(c1)
        self._board.add(c2)
        self._board.add(c3)
        print(f"Flop: {c1}, {c2}, {c3}")
        print(f"Board: {[x for x in self._board[:3]]}")

    def draw_turn(self, card=None):
        if len(self._board) != 3:
            raise ValueError("Board size must be 3 before we can draw a turn")
        card = self._deck.draw(card)
        self._board.add(card)
        print(f"Turn: {card}")
        print(f"Board: {[x for x in self._board[:4]]}")

    def draw_river(self, card=None):
        if len(self._board) != 4:
            raise ValueError("Board size must be 4 before we can draw a turn")
        card = self._deck.draw(card)
        self._board.add(card)
        print(f"River: {card}")
        print(f"Board: {[x for x in self._board[:5]]}")
