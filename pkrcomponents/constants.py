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
    BET = "BET", "bet", "bets", "BETS", "Bet", "Bets", "R"
    RAISE = "RAISE", "raise", "raises",  "RAISES", "Raise", "Raises", "R"
    CHECK = "CHECK", "check", "checks", "CHECKS", "Check", "Checks", "X"
    FOLD = "FOLD", "fold", "folded", "folds", "FOLDS", "Fold", "Folds", "F"
    CALL = "CALL", "call", "calls", "CALLS", "Call", "Calls", "C"
    RETURN = "RETURN", "return", "returned", "uncalled", "O"
    WIN = "WIN", "win", "won", "collected", "W"
    SHOW = "SHOW", "show", "shows", "SHOWS", "Show", "Shows", "S"
    MUCK = "MUCK", "MUCKS", "don't show", "didn't show", "did not show", "mucks", "does not show", "doesn't show", "M"
    THINK = "seconds left to act", "T"

    @property
    def symbol(self):
        return self._value_[len(self._value_)-1]


class Position(PokerEnum):
    """Class describing the table position"""
    UTG = "UTG", "under the gun"
    UTG1 = "UTG1", "utg+1", "utg + 1"
    UTG2 = "UTG2", "utg+2", "utg + 2"
    UTG3 = "UTG3", "utg+3", "utg + 3"
    UTG4 = "UTG4", "LJ", "lojack", "lowjack", "utg+4", "utg + 4"
    HJ = "HJ", "hijack", "highjack", "utg+5", "utg + 5"
    CO = "CO", "cutoff", "cut off", "cut-off"
    BTN = "BTN", "bu", "button"
    SB = "SB", "small blind"
    BB = "BB", "big blind"


class Street(PokerEnum):
    """Class describing the street"""
    PREFLOP = "PF", "Pf", "pf", "PREFLOP", "Preflop", "preflop", "Préflop", "préflop", "PreFlop",
    FLOP = "F", "f", "FLOP", "Flop", "flop"
    TURN = "T", "t", "TURN", "Turn", "turn"
    RIVER = "R", "r", "RIVER", "River", "river"
    SHOWDOWN = "SD", 'Sd', "sd", "SHOWDOWN", "ShowDown", "Showdown", "showdown"
