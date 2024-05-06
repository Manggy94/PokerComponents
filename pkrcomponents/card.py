from itertools import product
from functools import total_ordering

import random

from pkrcomponents._common import PokerEnum, _ReprMixin

__all__ = ["Suit", "Rank", "Card", "FACE_RANKS", "BROADWAY_RANKS", "Deck"]


class Suit(PokerEnum):
    """
    Suit of a card
    """
    CLUBS = "c", "clubs", "♣", "C"
    DIAMONDS = "d", "diamonds", "♦", "D"
    HEARTS = "h", "hearts", "♥", "H"
    SPADES = "s", "spades", "♠", "S"
    # Can't make alias with redefined value property
    # because of a bug in stdlib enum module (line 162)
    # C = '♣', 'c', 'C', 'clubs'


class Rank(PokerEnum):
    """
    Rank of a card
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
    JACK = ("J",)
    QUEEN = ("Q",)
    KING = ("K",)
    ACE = "A", 1

    @classmethod
    def difference(cls, first, second):
        """Tells the numerical difference between two ranks."""

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
    """Represents a Card, which consists a Rank and a Suit."""

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
    def is_face(self):
        """
        Indicates if the card is a face
        """
        return self.rank in FACE_RANKS

    @property
    def is_broadway(self):
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


class Deck:
    """A deck of cards"""

    def __init__(self):
        self.cards = list(Card)

    def __len__(self):
        return self.cards.__len__()

    def shuffle(self):
        """
        Randomly shuffles the deck
        """
        random.shuffle(self.cards)

    def reset(self):
        """Re-initializes the deck and shuffles it"""
        self.cards = list(Card)
        self.shuffle()

    def draw(self, cd=None):
        """
        Returns a card from the deck
        If the parameter card is given, it returns the card at stake and pops it from the deck
        """
        if not cd:
            return self.cards.pop()
        else:
            cd = Card(cd)
            idx = self.cards.index(cd)
            return self.cards.pop(idx)

    @property
    def len(self):
        """
        Returns the number of cards currently in the deck
        """
        return self.__len__()

    def to_json(self):
        return {
            "cards": [f"{card}" for card in self.cards],
            "len": self.len
        }
