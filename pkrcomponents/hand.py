import random
import pandas as pd
import numpy as np
from functools import total_ordering
from pkrcomponents._common import PokerEnum, _ReprMixin
from pkrcomponents.card import Rank, Card, BROADWAY_RANKS


__all__ = [
    "Shape",
    "Hand",
    "Combo",
    "ComboRange",
    "PAIR_HANDS",
    "OFFSUIT_HANDS",
    "SUITED_HANDS",
]


# pre generates all the possible suit combinations, so we don't have to count them all the time
_PAIR_SUIT_COMBINATIONS = ("cd", "ch", "cs", "dh", "ds", "hs")
_OFFSUIT_SUIT_COMBINATIONS = (
    "cd",
    "ch",
    "cs",
    "dc",
    "dh",
    "ds",
    "hc",
    "hd",
    "hs",
    "sc",
    "sd",
    "sh",
)
_SUITED_SUIT_COMBINATIONS = ("cc", "dd", "hh", "ss")


class Shape(PokerEnum):
    """
    Shape of a Hand
    """
    OFFSUIT = "o", "offsuit", "off"
    SUITED = "s", "suited"
    PAIR = "", "paired"

    @property
    def name(self):
        return self._name_

    @property
    def symbol(self):
        return self._value_[0]

    @property
    def adjective(self):
        return self._value_[1]


class _HandMeta(type):
    """Makes Hand class iterable. __iter__ goes through all hands in ascending order."""

    def __new__(mcs, clsname, bases, classdict):
        """Cache all possible Hand instances on the class itself."""
        cls = super(_HandMeta, mcs).__new__(mcs, clsname, bases, classdict)
        cls._all_hands = tuple(cls._get_non_pairs()) + tuple(cls._get_pairs())
        return cls

    def _get_non_pairs(cls):
        """Generator of all non-paired hands"""
        for rank1 in Rank:
            for rank2 in (rk for rk in Rank if rk < rank1):
                yield cls(f"{rank1}{rank2}o")
                yield cls(f"{rank1}{rank2}s")

    def _get_pairs(cls):
        """Generator of all paired hands"""
        for rank in Rank:
            yield cls(rank.val * 2)

    def __iter__(cls):
        return iter(cls._all_hands)


@total_ordering
class Hand(_ReprMixin, metaclass=_HandMeta):
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

    def to_combos(self):
        """Transforms a Hand into all its possible Combos"""
        first, second = self.first.val, self.second.val
        if self.is_pair:
            return tuple(
                Combo(first + s1 + first + s2) for s1, s2 in _PAIR_SUIT_COMBINATIONS
            )
        elif self.is_offsuit:
            return tuple(
                Combo(first + s1 + second + s2) for s1, s2 in _OFFSUIT_SUIT_COMBINATIONS
            )
        else:
            return tuple(
                Combo(first + s1 + second + s2) for s1, s2 in _SUITED_SUIT_COMBINATIONS
            )

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


PAIR_HANDS = tuple(hand for hand in Hand if hand.is_pair)
"""Tuple of all pair hands in ascending order."""

OFFSUIT_HANDS = tuple(hand for hand in Hand if hand.is_offsuit)
"""Tuple of offsuit hands in ascending order."""

SUITED_HANDS = tuple(hand for hand in Hand if hand.is_suited)
"""Tuple of suited hands in ascending order."""


@total_ordering
class Combo(_ReprMixin):
    """Hand combination, made of two cards"""

    _shape: Shape
    __slots__ = ("first", "second")

    def __new__(cls, combo):
        if isinstance(combo, Combo):
            return combo
        if not combo:
            return None
        if len(combo) != 4:
            raise ValueError(f"{combo}, should have a length of 4")
        elif combo[0] == combo[2] and combo[1] == combo[3]:
            raise ValueError(f"{combo!r}, Pair can't have the same suit: {combo[1]!r}")

        self = super().__new__(cls)
        self._set_cards_in_order(combo[:2], combo[2:])
        return self

    @classmethod
    def from_cards(cls, first, second):
        """Creates a Combo from two cards"""
        first, second = Card(first), Card(second)
        if first == second:
            raise ValueError("We cannot have the same card twice in a Combo")
        self = super().__new__(cls)
        first = first.rank.val + first.suit.val
        second = second.rank.val + second.suit.val
        self._set_cards_in_order(first, second)
        return self

    @classmethod
    def from_tuple(cls, combo_tuple):
        """
        Creates a combo from a tuple of cards
        """
        if not (isinstance(combo_tuple, tuple)):
            raise ValueError("A tuple should be given")
        if len(combo_tuple) != 2:
            raise ValueError("Tuple should contain two cards")
        first, second = combo_tuple[0], combo_tuple[1]
        return cls.from_cards(first, second)

    def __str__(self):
        return f"{self.first}{self.second}"

    def __hash__(self):
        return self.first.__hash__() + self.second.__hash__()

    def __eq__(self, other):
        if self.__class__ is not other.__class__:
            if isinstance(other, Hand):
                return self.to_hand() == other
            else:
                raise ValueError("You can only compare a Combo or a Hand with another Combo")
        return self.first == other.first and self.second == other.second

    def __lt__(self, other):
        if self.__class__ is not other.__class__:
            if isinstance(other, Hand):
                return self.to_hand() < other
            else:
                raise ValueError("You can only compare a Combo or a Hand with another Combo")
        return self.to_hand() < other.to_hand()

    def _set_cards_in_order(self, first, second):
        """Private method to order cards in a combo and prevent redundancies"""
        self.first, self.second = Card(first), Card(second)
        if self.first < self.second:
            self.first, self.second = self.second, self.first

    def to_hand(self):
        """Convert combo to :class:`Hand` object, losing suit information."""
        return Hand(f"{self.first.rank}{self.second.rank}{self.shape}")

    @property
    def is_suited_connector(self):
        """Indicates if the combo is a suited connector"""
        return self.is_suited and self.is_connector

    @property
    def is_suited(self):
        """Indicates if the combo is suited"""
        return self.first.suit == self.second.suit

    @property
    def is_offsuit(self):
        """Indicates if the combo is offsuit"""
        return not self.is_suited and not self.is_pair

    @property
    def is_connector(self):
        """Indicates if the combo is a connector"""
        return self.rank_difference == 1

    @property
    def is_one_gapper(self):
        """Indicates if the combo is a one gapper"""
        return self.rank_difference == 2

    @property
    def is_two_gapper(self):
        """Indicates if the combo is a two gapper"""
        return self.rank_difference == 3

    @property
    def rank_difference(self):
        """The difference between the first and second rank of the Combo."""
        # self.first >= self.second
        return Rank.difference(self.first.rank, self.second.rank)

    @property
    def is_pair(self):
        """Indicates if the combo is a pair"""
        return self.first.rank == self.second.rank

    @property
    def is_broadway(self):
        """Indicates if the combo is a broadway"""
        return self.first.is_broadway and self.second.is_broadway

    @property
    def shape(self):
        """Returns the shape of the combo"""
        if self.is_pair:
            return Shape.PAIR
        elif self.is_suited:
            return Shape.SUITED
        else:
            return Shape.OFFSUIT


class ComboRange(pd.DataFrame):
    """
    Class defining a Combo range, associating each combo possibility with a probability
    """
    def __init__(self):
        all_combos = np.hstack([hand.to_combos() for hand in list(Hand)])
        str_combos = [f"{combo}" for combo in all_combos]
        pd.DataFrame.__init__(self, index=str_combos, columns=["p"], data=1/1326)

    """def clean_range(self, dead_cards):
        cop = self.copy()
        indexes = self.index.to_numpy()
        cop["c1"] = np.array([f"{Combo(x).first}" for x in indexes])
        cop["c2"] = np.array([f"{Combo(x).second}" for x in indexes])
        cop["dead"] = cop["c1"].isin(dead_cards) | cop["c2"].isin(dead_cards)
        cop["p2"] = cop["p"] * ~cop["dead"]

        cop["p3"] = cop["p2"] / cop["p2"].sum()
        self["p"] = cop["p3"]
        del(cop, indexes)"""
