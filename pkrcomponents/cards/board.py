from attrs import define, field, Factory
from attrs.validators import instance_of, optional
import numpy as np
import pandas as pd
from pkrcomponents.cards.card import Card
from pkrcomponents.cards.flop import Flop
from pkrcomponents.utils.converters import convert_to_card


@define(eq=False)
class Board:
    flop = field(default=Factory(Flop), validator=instance_of(Flop))
    turn = field(default=None, validator=optional(instance_of(Card)), converter=convert_to_card)
    river = field(default=None, validator=optional(instance_of(Card)), converter=convert_to_card)

    @classmethod
    def from_cards(cls, cards=None):
        if cards is None:
            cards = []
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
        return self.flop == other.flop and self.turn == other.turn and self.river == other.river

    @property
    def cards(self):
        return pd.Series(
            data=self.flop.cards + [self.turn, self.river],
            index=["flop_1", "flop_2", "flop_3", "turn", "river"],
            name="cards"
        ).fillna(value=np.nan)

    @property
    def len(self):
        """
        Returns the number of cards on the board
        """
        return self.__len__()

    def add(self, card: [str, Card]):
        """
        Add a card to the board
        """
        card = Card(card)
        if len(self) == 5:
            raise ValueError("Board is already full with 5 cards")
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
        """
        Returns the board as a JSON
        """
        return self.cards.astype(str).to_dict()
