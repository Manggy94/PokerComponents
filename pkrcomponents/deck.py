"""This module contains the Deck class, which represents a deck of cards."""
import random
from pkrcomponents.card import Card


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

    def draw(self, card=None):
        """
        Returns a card from the deck
        If the parameter card is given, it returns the card at stake and pops it from the deck
        """
        if not card:
            return self.cards.pop()
        else:
            card = Card(card)
            idx = self.cards.index(card)
            return self.cards.pop(idx)

    def replace(self, card):
        """
        Replaces a card in the deck
        """
        if card not in self.cards:
            self.cards.append(card)

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
