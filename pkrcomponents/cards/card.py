"""This module contains the Card class, which represents a playing card.
It also contains the Rank and Suit classes, which are used to define the rank and suit of a card."""
from functools import total_ordering

from pkrcomponents.utils.common import _ReprMixin
from pkrcomponents.cards.rank import Rank
from pkrcomponents.cards.suit import Suit
from pkrcomponents.utils.meta.card_meta import CardMeta

__all__ = ["Card"]


@total_ordering
class Card(_ReprMixin, metaclass=CardMeta):
    """
    Represents a Card, which consists a Rank and a Suit.

    Attributes:
        rank (Rank): the rank of the card
        suit (Suit): the suit of the card

    Methods:
        is_face: indicates if the card is a face
        is_broadway: indicates if the card is a broadway
        make_random: returns a random Card instance

    """

    __slots__ = ("rank", "suit")

    def __new__(cls, card):
        if card is None:
            return None
        if isinstance(card, cls):
            return card
        elif isinstance(card, str):
            if len(card) != 2:
                raise ValueError(f"Length should be two in {card}")

            self = object.__new__(cls)
            self.rank = Rank(card[0])
            self.suit = Suit(card[1])
            return self
        else:
            raise TypeError("A card or string must be given")

    def __hash__(self):
        return hash(self.rank) + hash(self.suit)

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.rank == other.rank and self.suit == other.suit
        else:
            raise ValueError("Only a Card can be compared with another")

    def __lt__(self, other):
        if self.__class__ is not other.__class__:
            raise ValueError("Only a Card can be compared with another")
        # with same ranks, suit counts
        if self.rank == other.rank:
            return self.suit < other.suit
        return self.rank < other.rank

    def __str__(self):
        return f"{self.rank}{self.suit}"

    def __sub__(self, other):
        return self.rank - other.rank

    @property
    def symbol(self) -> str:
        return f"{self.rank.symbol}{self.suit.symbol}"

    @property
    def name(self) -> str:
        return f"{self.rank.name} of {self.suit.name}"

    @property
    def short_name(self) -> str:
        return f"{self.rank.symbol}{self.suit.short_name}"

    @property
    def is_face(self) -> bool:
        """
        Indicates if the card is a face
        """
        return self.rank.is_face

    @property
    def is_broadway(self) -> bool:
        """
        Indicates if the card is a broadway
        """
        return self.rank.is_broadway

    @classmethod
    def make_random(cls):
        """Returns a random Card instance."""
        self = object.__new__(cls)
        self.rank = Rank.make_random()
        self.suit = Suit.make_random()
        return self
