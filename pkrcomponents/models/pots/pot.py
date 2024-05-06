

from pkrcomponents.models.amount import Amount


class Pot:
    """Class representing the pot of a table"""
    _highest_bet: Amount
    _value: Amount

    def __init__(self):
        self.value = 0
        self.highest_bet = 0

    def add(self, amount: Amount):
        """Add an amount to the pot"""
        if amount < 0:
            raise ValueError("amount added to pot can only be positive")
        self.value += amount

    @property
    def value(self):
        """Returns pot's numerical value"""
        return self._value

    @value.setter
    def value(self, value):
        """Setter for value property"""
        self._value = value

    @property
    def highest_bet(self):
        """Returns current highest bet in this pot"""
        return self._highest_bet

    @highest_bet.setter
    def highest_bet(self, bet):
        """Setter for highest bet property"""
        self._highest_bet = bet

