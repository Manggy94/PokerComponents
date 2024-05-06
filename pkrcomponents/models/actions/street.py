from functools import cached_property

STREET_NAMES = ["PREFLOP", "FLOP", "TURN", "RIVER"]


class Street:
    """
    Class describing the street
    """
    name: str
    symbol: str
    short_name: str
    order: int

    def __init__(self, name: str):
        self.name = name

    @cached_property
    def symbol(self):
        """
        Symbol of the street
        """
        return self.name[0]

    @cached_property
    def short_name(self):
        """
        Short name of the street
        """
        return self.name.capitalize()

    @cached_property
    def order(self):
        """
        Order of the street
        """
        return STREET_NAMES.index(self.name) + 1
