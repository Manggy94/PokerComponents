from itertools import product, combinations
from pkrcomponents.card import Card
from pkrcomponents.shape import Shape


class ComboMeta(type):

    def __new__(mcs, clsname, bases, classdict):
        """Cache all possible Combo instances on the class itself."""
        cls = super(ComboMeta, mcs).__new__(mcs, clsname, bases, classdict)
        cls.all_combos = list(
            cls(f"{first}{second}")
            for first, second in combinations(Card.all_cards,2)

        )
        return cls

    def __iter__(cls):
        return iter(cls.all_combos)