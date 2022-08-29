from functools import cached_property
from itertools import combinations
import pandas as pd
from components.card import Card
from components.hand import Combo


class Board(pd.Series):

    def __init__(self, cards=()):
        pd.Series.__init__(self, index=["flop_1", "flop_2", "flop_3", "turn", "river"], dtype="<U8")
        for card in cards:
            self.add(card)

    def __len__(self):
        return 5 - self.isna().sum()

    def add(self, card):
        if len(self) == 5:
            raise ValueError("Board is already full with 5 cards")
        card = f"{Card(card)}"
        if self.isin([card]).any():
            raise ValueError("A same card cannot be put in the board twice or more")
        self.iloc[len(self)] = card

    @cached_property
    def flop_combinations(self):
        try:
            return [Combo.from_tuple(x) for x in combinations(self[:3], 2)]
        except IndexError:
            return None

    @cached_property
    def is_rainbow(self):
        if len(self.board) == 0:
            return None
        return all(
            first.suit != second.suit for first, second in self.flop_combinations
        )
