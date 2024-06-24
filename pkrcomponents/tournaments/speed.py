from pkrcomponents.utils.common import PokerEnum


class TourSpeed(PokerEnum):
    """Class describing the tournament speed"""
    SLOW = "Slow",
    REGULAR = "Regular", "normal"
    TURBO = "Turbo", "semiturbo"
    HYPER = "Hyper-Turbo", "turbo"
    DOUBLE = "2x-Turbo",
