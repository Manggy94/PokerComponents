from itertools import combinations
from pkrcomponents.cards.card import Card
from pkrcomponents.cards.rank import Rank
from pkrcomponents.utils.meta.flop_meta import FlopMeta


class Flop(metaclass=FlopMeta):
    """
    A class to represent a poker flop.
    """

    def __init__(self, first_card=None, second_card=None, third_card=None):
        try:
            self.first_card, self.second_card, self.third_card = sorted(
                (Card(card) for card in (first_card, second_card, third_card)), reverse=True
            )
        except TypeError:
            self.first_card, self.second_card, self.third_card = None, None, None

    def __eq__(self, other):
        return self.cards_set == other.cards_set

    def __repr__(self):
        return f"Flop('{self.first_card}{self.second_card}{self.third_card}')"

    @property
    def short_name(self):
        return f"{self.first_card.short_name}{self.second_card.short_name}{self.third_card.short_name}"

    @property
    def symbol(self):
        return f"{self.first_card.symbol}{self.second_card.symbol}{self.third_card.symbol}"

    @property
    def cards(self):
        return [self.first_card, self.second_card, self.third_card]

    @property
    def cards_set(self):
        return set(self.cards)

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
    def has_straight_draw(self):
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
