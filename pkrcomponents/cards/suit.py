from itertools import product, combinations
from pkrcomponents.utils.common import PokerEnum


class Suit(PokerEnum):
    """
    Suit of a card: Clubs, Diamonds, Hearts, Spades
    """
    CLUBS = "c", "clubs", "♣", "C"
    DIAMONDS = "d", "diamonds", "♦", "D"
    HEARTS = "h", "hearts", "♥", "H"
    SPADES = "s", "spades", "♠", "S"

    @classmethod
    def get_suit_combinations(cls):
        return tuple(product(cls, repeat=2))

    @classmethod
    def get_paired_suit_combinations(cls):
        return tuple(combinations(cls, 2))

    @classmethod
    def get_suited_suit_combinations(cls):
        return tuple((s, s) for s in cls)

    @classmethod
    def get_offsuit_suit_combinations(cls):
        return tuple((s1, s2) for s1, s2 in cls.get_suit_combinations() if s1 != s2)


    @property
    def symbol(self):
        return self._value_[2]

    @property
    def short_name(self):
        return self._value_[0]

    @property
    def name(self):
        return self._name_
