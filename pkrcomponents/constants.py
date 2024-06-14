from pkrcomponents._common import PokerEnum


class PokerRoom(PokerEnum):
    """Class describing famous online poker rooms"""
    STARS = "POKERSTARS", "PokerStars", "STARS", "PS"
    FTP = "Full Tilt Poker", "FTP", "FULL TILT"
    PKR = "PKR", "PKR POKER"
    EIGHT = "888", "888poker"
    WINA = "WINAMAX", "Winamax", "Wina", "WINA"


class Currency(PokerEnum):
    """Class describing used currency"""
    USD = "USD", "$"
    EUR = "EUR", "€"
    GBP = "GBP", "£"
    STARS_COIN = "SC", "StarsCoin"


class GameType(PokerEnum):
    """Class describing the format of game"""
    TOUR = "Tournament", "TOUR"
    CASH = "Cash game", "CASH", "RING"
    SNG = "Sit & Go", "SNG", "SIT AND GO", "Sit&go"


class Game(PokerEnum):
    """Class describing the variety of poker played"""
    HOLDEM = "Hold'em", "HOLDEM", "Holdem", "Holdem no limit"
    OMAHA = ("Omaha",)
    OHILO = ("Omaha Hi/Lo",)
    RAZZ = ("Razz",)
    STUD = ("Stud",)


class Limit(PokerEnum):
    """Class describing pot format"""
    NL = "NL", "No limit"
    PL = "PL", "Pot limit"
    FL = "FL", "Fixed limit", "Limit"


class TourFormat(PokerEnum):
    """Class describing the tournament format"""
    ONEREB = ("1R1A",)
    REBUY = "Rebuy", "+R"
    SECOND = ("2x Chance",)
    ACTION = ("Action Hour",)


class TourSpeed(PokerEnum):
    """Class describing the tournament speed"""
    SLOW = ("Slow",)
    REGULAR = ("Regular",)
    TURBO = ("Turbo",)
    HYPER = ("Hyper-Turbo",)
    DOUBLE = ("2x-Turbo",)


class MoneyType(PokerEnum):
    """Class describing money type"""
    REAL = "Real money", "Real", "real"
    PLAY = "Play money", "Play", "play"


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


class Position(PokerEnum):
    """Class describing the table position"""
    UTG = "UTG", 1, 3, "under the gun"
    UTG1 = "UTG1", 2, 4, "utg+1", "utg + 1"
    UTG2 = "UTG2", 3, 5, "utg+2", "utg + 2"
    UTG3 = "UTG3", 4, 6, "utg+3", "utg + 3"
    LJ = "LJ", 5, 7, "UTG4", "lojack", "lowjack", "utg+4", "utg + 4"
    HJ = "HJ", 6, 8, "hijack", "highjack", "utg+5", "utg + 5"
    CO = "CO", 7, 9, "cutoff", "cut off", "cut-off"
    BTN = "BTN", 8, 10, "bu", "button"
    SB = "SB", 9, 1, "small blind"
    BB = "BB", 10, 2, "big blind"

    @property
    def name(self):
        return self._name_

    @property
    def short_name(self):
        return self.name

    @property
    def symbol(self):
        return self.name

    @property
    def is_early(self):
        return self.name in ["UTG", "UTG1", "UTG2", "UTG3"]

    @property
    def is_middle(self):
        return self.name in ["LJ", "HJ"]

    @property
    def is_late(self):
        return self.name in ["CO", "BTN"]

    @property
    def is_blind(self):
        return self.name in ["SB", "BB"]

    @property
    def preflop_order(self):
        return self._value_[1]

    @property
    def postflop_order(self):
        return self._value_[2]


class Street(PokerEnum):
    """Class describing the street"""
    PREFLOP = "PF", "PreFlop", "Pf", "pf", "PREFLOP", "Preflop", "preflop", "Préflop", "préflop",
    FLOP = "F", "Flop", "f", "FLOP", "flop"
    TURN = "T", "Turn", "t", "TURN", "turn"
    RIVER = "R", "River", "r", "RIVER", "river"
    SHOWDOWN = "SD", "ShowDown", 'Sd', "sd", "SHOWDOWN", "Showdown", "showdown"

    @property
    def symbol(self):
        return self._value_[0]

    @property
    def name(self):
        return self._name_

    @property
    def parsing_name(self):
        return self._value_[1]

    @property
    def short_name(self):
        return self._value_[0]

    @property
    def is_preflop(self):
        return self.name == "PREFLOP"
