from functools import cached_property

SUIT_NAMES = ["CLUBS", "DIAMONDS", "HEARTS", "SPADES"]
SUIT_SYMBOLS = ["♣", "♦", "♥", "♠"]


class Suit:
    """
    A model to describe poker cards suits
    """
    name: str
    symbol: str
    short_name: str
    pk: int

    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}')"

    def __lt__(self, other):
        return self.pk < other.pk

    @cached_property
    def short_name(self):
        """
        Returns the short name of the suit
        """
        return self.name[0].lower()

    @cached_property
    def pk(self):
        """
        Returns the primary key of the suit
        """
        return SUIT_NAMES.index(self.name) + 1
