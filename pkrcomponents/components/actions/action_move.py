from pkrcomponents.components.utils.common import PokerEnum


class ActionMove(PokerEnum):
    """
    Class describing an action done

    Attributes:
        FOLD (str): The player folds
        CHECK (str): The player checks
        CALL (str): The player calls
        BET (str): The player bets
        RAISE (str): The player raises

    """
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
        """
        Returns:
            (str): The name of the action
        """
        return self._name_

    @property
    def symbol(self):
        """
        Returns:
            (str): The symbol of the action
        """
        return self._value_[0]

    @property
    def is_call_move(self):
        """
        Returns:
            (bool): True if the action is a call or a check
        """
        return self.symbol in ["C", "X"]

    @property
    def is_bet_move(self):
        """
        Returns:
            (bool): True if the action is a bet or a raise
        """
        return self.symbol in ["B", "R"]

    @property
    def is_vpip_move(self):
        """
        Returns:
            (bool): True if the action is a call, bet or raise
        """
        return self.symbol in ["C", "B", "R"]

    @property
    def verb(self):
        return self._value_[2]

    def __str__(self):
        return self.symbol
