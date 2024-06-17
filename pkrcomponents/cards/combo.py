from functools import total_ordering
from pkrcomponents.utils.common import _ReprMixin
from pkrcomponents.cards.card import Card
from pkrcomponents.cards.hand import Hand
from pkrcomponents.cards.rank import Rank
from pkrcomponents.cards.shape import Shape
from pkrcomponents.cards.suit import Suit
from pkrcomponents.utils.meta.combo_meta import ComboMeta


@total_ordering
class Combo(_ReprMixin, metaclass=ComboMeta):
    """Hand combination, made of two cards"""

    _shape: Shape
    __slots__ = ("first", "second")

    def __new__(cls, combo):
        if isinstance(combo, cls):
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
                return self.hand == other
            else:
                raise ValueError("You can only compare a Combo or a Hand with another Combo")
        return self.first == other.first and self.second == other.second

    def __lt__(self, other):
        if self.__class__ is not other.__class__:
            if isinstance(other, Hand):
                return self.hand < other
            else:
                raise ValueError("You can only compare a Combo or a Hand with another Combo")
        return self.hand < other.hand

    def _set_cards_in_order(self, first, second):
        """Private method to order cards in a combo and prevent redundancies"""
        self.first, self.second = Card(first), Card(second)
        if self.first < self.second:
            self.first, self.second = self.second, self.first

    @property
    def hand(self):
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

    @classmethod
    def from_hand(cls, hand: Hand):
        """Creates a Combo from a Hand"""
        if hand.is_pair:
            combinations_function = Suit.get_paired_suit_combinations
        elif hand.is_offsuit:
            combinations_function = Suit.get_offsuit_suit_combinations
        else:
            combinations_function = Suit.get_suited_suit_combinations
        return tuple(Combo(f"{hand.first}{suit1}{hand.second}{suit2}") for suit1, suit2 in combinations_function())
