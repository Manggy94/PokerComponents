"""This module contains the Card class, which represents a playing card.
It also contains the Rank and Suit classes, which are used to define the rank and suit of a card."""
from itertools import product
from functools import total_ordering

from pkrcomponents._common import PokerEnum, _ReprMixin

__all__ = ["Suit", "Rank", "Card", "FACE_RANKS", "BROADWAY_RANKS"]


class Suit(PokerEnum):
    """
    Suit of a card: Clubs, Diamonds, Hearts, Spades
    """
    CLUBS = "c", "clubs", "♣", "C"
    DIAMONDS = "d", "diamonds", "♦", "D"
    HEARTS = "h", "hearts", "♥", "H"
    SPADES = "s", "spades", "♠", "S"

    @property
    def symbol(self):
        return self._value_[2]

    @property
    def short_name(self):
        return self._value_[0]

    @property
    def name(self):
        return self._name_


class Rank(PokerEnum):
    """
    Rank of a card in a deck, from 2 to Ace.

    Methods:
        difference: tells the numerical difference between two ranks
    """
    DEUCE = "2", 2
    THREE = "3", 3
    FOUR = "4", 4
    FIVE = "5", 5
    SIX = "6", 6
    SEVEN = "7", 7
    EIGHT = "8", 8
    NINE = "9", 9
    TEN = "T", 10
    JACK = "J", 11
    QUEEN = "Q", 12
    KING = "K", 13
    ACE = "A", 1

    @property
    def symbol(self):
        return self.value[0]

    def __str__(self):
        return self.symbol

    @property
    def name(self):
        return self._name_

    @classmethod
    def difference(cls, first, second) -> int:
        """
        Tells the numerical difference between two ranks.

        Args:
            first (Rank): the first rank
            second (Rank): the second rank

        Returns:
            int: the difference between the two ranks
        """

        # so we always get a Rank instance even if string were passed in
        first, second = cls(first), cls(second)
        rank_list = list(cls)
        a = rank_list.index(first)+2
        b = rank_list.index(second)+2
        if a == 14:
            return min(abs(a-b), abs(1-b))
        elif b == 14:
            return min(abs(a - b), abs(a - 1))
        return abs(rank_list.index(first) - rank_list.index(second))

    def __sub__(self, other):
        return self.difference(self, other)


FACE_RANKS = Rank("J"), Rank("Q"), Rank("K")

BROADWAY_RANKS = Rank("T"), Rank("J"), Rank("Q"), Rank("K"), Rank("A")


class _CardMeta(type):
    def __new__(mcs, clsname, bases, classdict):
        """Cache all possible Card instances on the class itself."""
        cls = super(_CardMeta, mcs).__new__(mcs, clsname, bases, classdict)
        cls._all_cards = list(
            cls(f"{rank}{suit}") for rank, suit in product(Rank, Suit)
        )
        return cls

    def __iter__(cls):
        return iter(cls._all_cards)


@total_ordering
class Card(_ReprMixin, metaclass=_CardMeta):
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
        if isinstance(card, cls):
            return card
        elif isinstance(card, str):
            if len(card) != 2:
                raise ValueError(f"length should be two in {card}")

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
    def is_face(self) -> bool:
        """
        Indicates if the card is a face
        """
        return self.rank in FACE_RANKS

    @property
    def is_broadway(self) -> bool:
        """
        Indicates if the card is a broadway
        """
        return self.rank in BROADWAY_RANKS

    @classmethod
    def make_random(cls):
        """Returns a random Card instance."""
        self = object.__new__(cls)
        self.rank = Rank.make_random()
        self.suit = Suit.make_random()
        return self


