from pkrcomponents.utils.common import PokerEnum


class TourSpeed(PokerEnum):
    """Class describing the tournament speed"""
    SLOW = ("Slow",)
    REGULAR = ("Regular",)
    TURBO = ("Turbo",)
    HYPER = ("Hyper-Turbo",)
    DOUBLE = ("2x-Turbo",)
