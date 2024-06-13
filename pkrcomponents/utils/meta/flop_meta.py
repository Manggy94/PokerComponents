from itertools import combinations
from pkrcomponents.card import Card


class FlopMeta(type):
    def __new__(mcs, clsname, bases, classdict):
        """Cache all possible Flop instances on the class itself."""
        cls = super(FlopMeta, mcs).__new__(mcs, clsname, bases, classdict)
        cls.all_flops = list(
            cls(
                first_card=first_card,
                second_card=second_card,
                third_card=third_card
            )
            for first_card, second_card, third_card in combinations(Card.all_cards, 3)
        )
        return cls

    def __iter__(cls):
        return iter(cls.all_flops)
