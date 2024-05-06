from functools import cached_property

MOVE_NAMES = ["FOLD", "CHECK", "CALL", "BET", "RAISE"]
MOVE_SYMBOLS = ["F", "X", "C", "B", "R"]
MOVE_VERBS = ["folds", "checks", "calls", "bets", "raises"]


class Move:
    """
    A class to describe poker Action moves
    """
    name: str
    symbol: str
    verb: str
    is_call_move: bool
    is_bet_move: bool
    is_vpip_move:  bool

    def __init__(self, name, symbol, verb):
        self.name = name
        self.symbol = symbol
        self.verb = verb

    @cached_property
    def is_call_move(self):
        """
        Indicates if a move is a call move
        """
        return self.name in ["CHECK", "CALL"]

    @cached_property
    def is_bet_move(self):
        return self.name in ["BET", "RAISE"]

    @cached_property
    def is_vpip_move(self):
        return self.name in ["CALL", "BET", "RAISE"]


