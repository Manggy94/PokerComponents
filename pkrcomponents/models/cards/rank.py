from functools import cached_property

RANK_NAMES = ["DEUCE", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE", "TEN", "JACK", "QUEEN", "KING", "ACE"]
RANK_SYMBOLS = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]


class Rank:
    """
    A model to describe poker cards ranks
    """
    pk: int
    name: str
    symbol: str
    short_name: str
    is_broadway: bool
    is_face: bool

    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.symbol}')"

    @cached_property
    def pk(self):
        return RANK_NAMES.index(self.name) + 1

    @cached_property
    def short_name(self):
        return self.symbol

    @cached_property
    def is_broadway(self):
        return self.pk >= 9

    @cached_property
    def is_face(self):
        return self.pk in (10, 11, 12)

    @classmethod
    def difference(cls, first, second):
        """
        Returns the difference between two ranks
        """
        a = first.pk + 1
        b = second.pk + 1
        if a == 14:
            return min(abs(a - b), abs(1 - b))
        elif b == 14:
            return min(abs(a - b), abs(a - 1))
        return abs(first.pk - second.pk)

    def __sub__(self, other):
        return self.difference(self, other)

    def __lt__(self, other):
        return self.pk < other.pk
