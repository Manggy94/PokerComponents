from pkrcomponents.models.cards.rank import Rank
from pkrcomponents.models.cards.suit import Suit


class Card:
    """
    A model to describe poker cards
    """

    rank: Rank
    suit: Suit
    symbol: str
    is_broadway: bool
    is_face: bool
    short_name: str

    @classmethod
    def from_string(cls, card_str: str):
        """
        Returns a Card object from a string
        """
        if len(card_str) != 2:
            raise ValidationError(f"length should be two in {card_str}")
        rank, suit = card_str
        rank = Rank.objects.get(symbol=rank)
        suit = Suit.objects.get(short_name=suit)
        return cls.objects.get(rank=rank, suit=suit)

    def __str__(self):
        return f"{self.rank}{self.suit}"

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.short_name}')"