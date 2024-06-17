from pkrcomponents.utils.common import PokerEnum


class ActionMove(PokerEnum):
    """Class describing an action done"""
    FOLD = "F", "fold", "folds", "FOLDS", "Fold", "Folds", "folded",
    CHECK = "X", "check", "checks", "CHECKS", "Check", "Checks"
    CALL = "C", "call", "calls", "CALLS", "Call", "Calls"
    BET = "B", "bet", "bets", "BETS", "Bet", "Bets"
    RAISE = "R", "raise", "raises",  "RAISES", "Raise", "Raises"

    RETURN = "O", "return", "returned", "uncalled"
    WIN = "W", "win", "won", "collected"
    SHOW = "S", "show", "shows", "SHOWS", "Show", "Shows"
    MUCK = "M", "MUCKS", "don't show", "didn't show", "did not show", "mucks", "does not show", "doesn't show"
    THINK = "T", "seconds left to act"

    @property
    def name(self):
        return self._name_

    @property
    def symbol(self):
        return self._value_[0]

    @property
    def is_call_move(self):
        return self.symbol in ["C", "X"]

    @property
    def is_bet_move(self):
        return self.symbol in ["B", "R"]

    @property
    def is_vpip_move(self):
        return self.symbol in ["C", "B", "R"]

    @property
    def verb(self):
        return self._value_[2]

    def __str__(self):
        return self.symbol
