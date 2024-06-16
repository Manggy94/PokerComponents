"""The Pot class represents the pot of a table. It has two attributes: value and highest_bet.
The value attribute represents the total amount of money in the pot,
while the highest_bet attribute represents the highest bet made by a player in the current round.
The Pot class has two methods: add and reset.
The add method adds an amount to the pot, while the reset method resets the pot to its initial state."""

from attrs import define, field
from attrs.validators import instance_of, ge


@define
class Pot:
    """
    This class represents the pot of a table

    Attributes:
        value (float): The value of the pot
        highest_bet (float): The highest bet made by a player in the current round

    Methods:
        add(amount): Add an amount to the pot
        reset(): Reset the pot
    """
    value = field(default=0.0, validator=[ge(0), instance_of(float, )], converter=float)
    highest_bet = field(default=0.0, validator=[ge(0), instance_of(float)], converter=float)

    def add(self, amount: float):
        """
        Add an amount to the pot

        Args:
            amount (float): The amount to add to the pot
        """
        if amount < 0:
            raise ValueError("amount added to pot can only be positive")
        self.value += amount

    def update_highest_bet(self, amount: float):
        """
        Update the highest bet in the pot

        Args:
            amount (float): The amount to compare with the current highest bet
        """
        if amount < 0:
            raise ValueError("amount added to pot can only be positive")
        if amount > self.highest_bet:
            self.highest_bet = amount

    def reset(self) -> None:
        """Reset the pot"""
        self.value = 0
        self.highest_bet = 0
