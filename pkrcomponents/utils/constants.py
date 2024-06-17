from pkrcomponents.utils.common import PokerEnum


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


class MoneyType(PokerEnum):
    """Class describing money type"""
    REAL = "Real money", "Real", "real"
    PLAY = "Play money", "Play", "play"


