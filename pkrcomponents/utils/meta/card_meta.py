from itertools import product

from pkrcomponents.cards.rank import Rank
from pkrcomponents.cards.suit import Suit


class CardMeta(type):
    def __new__(mcs, clsname, bases, classdict):
        """Cache all possible Card instances on the class itself."""
        cls = super(CardMeta, mcs).__new__(mcs, clsname, bases, classdict)
        cls.all_cards = list(
            cls(f"{rank}{suit}") for rank, suit in product(Rank, Suit)
        )
        return cls

    def __iter__(cls):
        return iter(cls.all_cards)

    def __len__(cls):
        return len(cls.all_cards)
