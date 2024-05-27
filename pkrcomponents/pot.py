"""The Pot class represents the pot of a table. It has two attributes: value and highest_bet.
The value attribute represents the total amount of money in the pot,
while the highest_bet attribute represents the highest bet made by a player in the current round.
The Pot class has two methods: add and reset.
The add method adds an amount to the pot, while the reset method resets the pot to its initial state."""

from attrs import define, field
from attrs.validators import instance_of, ge


@define
class Pot:
    """Class representing the pot of a table"""
    value = field(default=0.0, validator=[ge(0), instance_of((float, int))])
    highest_bet = field(default=0.0, validator=[ge(0), instance_of((float, int))])

    def add(self, amount):
        """Add an amount to the pot"""
        if amount < 0:
            raise ValueError("amount added to pot can only be positive")
        self.value += amount

    def reset(self):
        """Reset the pot"""
        self.value = 0
        self.highest_bet = 0
