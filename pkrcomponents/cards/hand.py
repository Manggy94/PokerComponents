import random
from functools import total_ordering
from pkrcomponents.utils.common import _ReprMixin
from pkrcomponents.cards.rank import Rank, FACE_RANKS, BROADWAY_RANKS

__all__ = [
    "Hand",
]

from pkrcomponents.cards.shape import Shape
from pkrcomponents.utils.meta.hand_meta import HandMeta


@total_ordering
class Hand(_ReprMixin, metaclass=HandMeta):
    """General hand without a precise suit. Only knows about two ranks and shape."""

    _shape: Shape

    __slots__ = ("first", "second", "_shape")

    def __new__(cls, hand):
        if isinstance(hand, cls):
            return hand

        if len(hand) not in (2, 3):
            raise ValueError("Length should be 2 (pair) or 3 (hand)")

        first, second = hand[:2]

        self = object.__new__(cls)

        if len(hand) == 2:
            if first != second:
                raise ValueError(
                    f"{hand} is not a pair! Maybe you need to specify a suit?"
                )
            self._shape = ""
        else:
            shape = hand[2].lower()
            if first == second:
                raise ValueError(f"{hand!r}; pairs can't have a suit: {shape!r}")
            if shape not in ("s", "o"):
                raise ValueError(f"{hand!r}; Invalid shape: {shape!r}")
            self._shape = shape

        self._set_ranks_in_order(first, second)

        return self

    def __str__(self):
        return f"{self.first}{self.second}{self.shape}"

    def __hash__(self):
        return hash(self.first) + hash(self.second) + hash(self.shape)

    def __eq__(self, other):
        if self.__class__ is not other.__class__:
            raise ValueError("You can only compare a Hand with another Hand")

        # AKs != AKo, because AKs is better
        return (
            self.first == other.first
            and self.second == other.second
            and self.shape.val == other.shape.val
        )

    def __lt__(self, other):
        if self.__class__ is not other.__class__:
            raise ValueError("You can only compare a Hand with another Hand")

        # pairs are better than non-pairs
        if not self.is_pair and other.is_pair:
            return True
        elif self.is_pair and not other.is_pair:
            return False
        elif (
            not self.is_pair
            and not other.is_pair
            and self.first == other.first
            and self.second == other.second
            and self.shape != other.shape
        ):
            # when Rank match, only suit is the deciding factor
            # so, offsuit hand is 'less' than suited
            return self._shape == "o"
        elif self.first == other.first:
            return self.second < other.second
        else:
            return self.first < other.first

    def _set_ranks_in_order(self, first, second):
        """
        Orders the two ranks of the hand
        """
        # set as Rank objects.
        self.first, self.second = Rank(first), Rank(second)
        if self.first < self.second:
            self.first, self.second = self.second, self.first

    @classmethod
    def make_random(cls):
        """
        Creates a random Hand
        """
        obj = object.__new__(cls)
        first = Rank.make_random()
        second = Rank.make_random()
        obj._set_ranks_in_order(first, second)
        if first == second:
            obj._shape = ""
        else:
            obj._shape = random.choice(["s", "o"])
        return obj

    @property
    def short_name(self):
        """Returns the short name of the hand"""
        return f"{self}"

    @property
    def symbol(self):
        """Returns the symbol of the hand"""
        return f"{self}"

    @property
    def is_suited_connector(self):
        """Indicates if the hand is a suited connector"""
        return self.is_suited and self.is_connector

    @property
    def is_suited(self):
        """Indicates if the hand is suited"""
        return self._shape == "s"

    @property
    def is_offsuit(self):
        """Indicates if the hand is offsuit"""
        return self._shape == "o"

    @property
    def is_connector(self):
        """Indicates if the hand is a connector"""
        return self.rank_difference == 1

    @property
    def is_one_gapper(self):
        """Indicates if the hand is a one gapper"""
        return self.rank_difference == 2

    @property
    def is_two_gapper(self):
        """Indicates if the hand is a two gapper"""
        return self.rank_difference == 3

    @property
    def rank_difference(self):
        """The difference between the first and second rank of the Hand."""
        return Rank.difference(self.first, self.second)

    @property
    def is_broadway(self):
        """Indicates if the hand is composed of 2 broadways"""
        return self.first in BROADWAY_RANKS and self.second in BROADWAY_RANKS

    @property
    def is_face(self):
        """Indicates if the hand is composed of 2 face cards"""
        return self.first in FACE_RANKS and self.second in FACE_RANKS

    @property
    def is_pair(self):
        """Indicates if the hand is a pair"""
        return self.first == self.second

    @property
    def shape(self):
        """
        Returns hand shape
        """
        return Shape(self._shape)

    @shape.setter
    def shape(self, value):
        """
        Setter for shape property
        """
        self._shape = Shape(value).val
