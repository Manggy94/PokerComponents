"""This module contains the Deck class, which represents a deck of cards."""
import random
from pkrcomponents.cards.card import Card


class Deck:
    """
    A class that represents a deck of cards

    Attributes:
        cards (list): the list of cards in the deck

    Methods:
        shuffle: randomly shuffles the deck
        reset: re-initializes the deck and shuffles it
        draw: returns a card from the deck
        replace: replaces a card in the deck
        to_json: returns the deck as a json object

    """

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

    def draw(self, card: (str, Card) = None):
        """
        Returns a card from the deck
        If the parameter card is given, it returns the card at stake and pops it from the deck

        Args:
            card (Card): the card to be drawn
        """
        if not card:
            return self.cards.pop()
        else:
            card = Card(card)
            idx = self.cards.index(card)
            return self.cards.pop(idx)

    def replace(self, card: Card):
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
