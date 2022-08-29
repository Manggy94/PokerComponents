from functools import cached_property
from itertools import combinations

import numpy as np
import pandas as pd
from components.card import Card, Rank
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
            return np.array([Combo.from_tuple(x) for x in combinations(self[:3], 2)])
        except IndexError:
            return None

    @cached_property
    def is_rainbow(self):
        if len(self) == 0:
            return None
        return all(
            combo.first.suit != combo.second.suit for combo in self.flop_combinations
        )

    def _get_differences(self):
        return tuple(Rank.difference(combo.first.rank, combo.second.rank)for combo in self.flop_combinations)

    @cached_property
    def is_monotone(self):
        if len(self) == 0:
            return None
        return all(combo.first.suit == combo.second.suit for combo in self.flop_combinations)

    @cached_property
    def is_triplet(self):
        if len(self) == 0:
            return None
        return all(diff == 0 for diff in self._get_differences())

    @cached_property
    def has_pair(self):
        if len(self) == 0:
            return None
        return any(diff == 0 for diff in self._get_differences())

    @cached_property
    def has_straightdraw(self):
        if len(self) == 0:
            return None
        return any(1 <= diff <= 3 for diff in self._get_differences())

    @cached_property
    def has_gutshot(self):
        if len(self) == 0:
            return None
        return any(1 <= diff <= 4 for diff in self._get_differences())

    @cached_property
    def has_flushdraw(self):
        if len(self) == 0:
            return None
        return any(combo.first.suit == combo.second.suit for combo in self.flop_combinations)