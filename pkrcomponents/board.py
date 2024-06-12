from itertools import combinations

from attrs import define, field, Factory
from attrs.validators import instance_of, optional
import numpy as np
import pandas as pd
from pkrcomponents.card import Card, Rank
from pkrcomponents.hand import Combo
from pkrcomponents.utils.converters import convert_to_card


@define
class Flop:
    """
    A class to represent a poker flop.
    """
    first_card: Card = field(default=None, validator=optional(instance_of(Card)), converter=convert_to_card)
    second_card: Card = field(default=None, validator=optional(instance_of(Card)), converter=convert_to_card)
    third_card: Card = field(default=None, validator=optional(instance_of(Card)), converter=convert_to_card)

    @property
    def short_name(self):
        return f"{self.first_card.short_name}{self.second_card.short_name}{self.third_card.short_name}"

    @property
    def cards(self):
        return [self.first_card, self.second_card, self.third_card]

    @property
    def suits(self):
        return {card.suit for card in self.cards}

    @property
    def ranks(self):
        return {card.rank for card in self.cards}

    @property
    def duos(self):
        return list(combinations(self.cards, 2))

    @property
    def differences(self):
        return {Rank.difference(duo[0].rank, duo[1].rank) for duo in self.duos}

    @property
    def is_rainbow(self):
        return len(self.suits) == 3

    @property
    def has_flush_draw(self):
        return len(self.suits) <= 2

    @property
    def is_monotone(self):
        return len(self.suits) == 1

    @property
    def is_triplet(self):
        return len(self.ranks) == 1

    @property
    def is_paired(self):
        return len(self.ranks) <= 2

    @property
    def min_distance(self):
        return min(self.differences)

    @property
    def max_distance(self):
        return max(self.differences)

    @property
    def has_straightdraw(self):
        return any(1 <= diff <= 3 for diff in self.differences)

    @property
    def has_gutshot(self):
        return any(1 <= diff <= 4 for diff in self.differences)

    @property
    def is_sequential(self):
        return self.differences == {1, 2}

    @property
    def has_straights(self):
        return len(self.ranks) == 3 and max(self.differences) <= 4

    def reset(self):
        """
        Reset the flop
        """
        self.first_card = None
        self.second_card = None
        self.third_card = None


@define
class Board:
    flop = field(default=Factory(Flop), validator=instance_of(Flop))
    turn = field(default=None, validator=optional(instance_of(Card)), converter=convert_to_card)
    river = field(default=None, validator=optional(instance_of(Card)), converter=convert_to_card)

    @classmethod
    def from_cards(cls, cards=[]):
        if len(cards) not in [0, 3, 4, 5]:
            raise ValueError("Board must have 0, 3, 4 or 5 cards")
        if len(cards) != len(set(cards)):
            raise ValueError("A same card cannot be put in the board twice or more")
        if len(cards) == 0:
            return cls()
        if len(cards) == 3:
            return cls(flop=Flop(*cards))
        if len(cards) == 4:
            return cls(flop=Flop(*cards[:3]), turn=Card(cards[3]))
        if len(cards) == 5:
            return cls(flop=Flop(*cards[:3]), turn=Card(cards[3]), river=Card(cards[4]))

    def __len__(self):
        return 5 - self.cards.isna().sum()

    def __eq__(self, other):
        return self.to_json() == other.to_json()

    @property
    def cards(self):
        return pd.Series(
            data=self.flop.cards + [self.turn, self.river],
            index=["flop_1", "flop_2", "flop_3", "turn", "river"],
            dtype="<U8",
            name="cards"
        ).fillna(value=np.nan)

    @property
    def len(self):
        """
        Returns the number of cards on the board
        """
        return self.__len__()

    def add(self, card):
        """
        Add a card to the board
        """
        if len(self) == 5:
            raise ValueError("Board is already full with 5 cards")
        card = f"{Card(card)}"
        if self.cards.isin([card]).any():
            raise ValueError("A same card cannot be put in the board twice or more")
        if len(self) == 0:
            self.flop.first_card = card
        elif len(self) == 1:
            self.flop.second_card = card
        elif len(self) == 2:
            self.flop.third_card = card
        elif len(self) == 3:
            self.turn = card
        else:
            self.river = card

    def reset(self):
        """
        Reset the board
        """
        self.flop.reset()
        self.turn = None
        self.river = None

    def to_json(self):
        return self.cards.astype(str).to_dict()
