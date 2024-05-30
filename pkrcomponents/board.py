from functools import cached_property
from itertools import combinations

import numpy as np
import pandas as pd
from pkrcomponents.card import Card, Rank
from pkrcomponents.hand import Combo


class Board(pd.Series):

    def __init__(self, cards=()):
        pd.Series.__init__(self, index=["flop_1", "flop_2", "flop_3", "turn", "river"], dtype="<U8")
        for card in cards:
            self.add(card)

    def __len__(self):
        return 5 - self.isna().sum()

    def __eq__(self, other):
        return self.to_json() == other.to_json()

    @property
    def len(self):
        """
        Returns the number of cards on the board
        """
        return self.__len__()

    @property
    def flop(self):
        """
        Returns the cards drawn at flop
        """
        return self.iloc[:3]

    @property
    def turn(self):
        """
        Returns the turn card
        """
        return self.iloc[3]

    @property
    def river(self):
        """
        Returns the river card
        """
        return self.iloc[4]

    def add(self, card):
        """
        Add a card to the board
        """
        if len(self) == 5:
            raise ValueError("Board is already full with 5 cards")
        card = f"{Card(card)}"
        if self.isin([card]).any():
            raise ValueError("A same card cannot be put in the board twice or more")
        self.iloc[len(self)] = card

    @cached_property
    def flop_combinations(self):
        """
        Returns an array of all the combos from the flop
        """
        try:
            return np.array([Combo.from_tuple(x) for x in combinations(self[:3], 2)])
        except TypeError:
            return None

    @cached_property
    def is_rainbow(self):
        """Boolean indicating if flop is rainbow"""
        if len(self) < 3:
            return None
        return all(
            combo.first.suit != combo.second.suit for combo in self.flop_combinations
        )

    def _get_differences(self):
        """Returns a tuple of differences between flop cards"""
        if self.flop_combinations is None:
            return None
        return tuple(Rank.difference(combo.first.rank, combo.second.rank)for combo in self.flop_combinations)

    @cached_property
    def is_monotone(self):
        """
        Boolean indicating if flop is monotone
        """
        if len(self) < 3:
            return None
        return all(combo.first.suit == combo.second.suit for combo in self.flop_combinations)

    @cached_property
    def is_triplet(self):
        """Boolean indicating if flop is triplet"""
        if len(self) < 3:
            return None
        return all(diff == 0 for diff in self._get_differences())

    @cached_property
    def has_pair(self):
        """
        Boolean indicating if flop has a pair
        """
        if len(self) < 3:
            return None
        return any(diff == 0 for diff in self._get_differences())

    @cached_property
    def has_straightdraw(self):
        """
        Boolean indicating if flop has a straightdraw
        """
        if len(self) < 3:
            return None
        return any(1 <= diff <= 3 for diff in self._get_differences())

    @cached_property
    def has_gutshot(self):
        """
        Boolean indicating if flop has a gutshot
        """
        if len(self) < 3:
            return None
        return any(1 <= diff <= 4 for diff in self._get_differences())

    @cached_property
    def has_flushdraw(self):
        """
        Boolean indicating if flop has a flushdraw
        """
        if len(self) < 3:
            return None
        return any(combo.first.suit == combo.second.suit for combo in self.flop_combinations)

    def reset(self):
        """
        Reset the board
        """
        self.iloc[:] = np.nan

    def to_json(self):
        return self.astype(str).to_dict()

