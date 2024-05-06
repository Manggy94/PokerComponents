from _decimal import Decimal, ROUND_HALF_UP


class Amount:
    """A class that represents the amounts that are paid or received by players"""
    value: Decimal

    def __init__(self, value):
        if isinstance(value, Amount):
            self._value = value.value
        elif isinstance(value, Decimal):
            self._value = value.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
        else:
            self._value = Decimal(value).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)

    @property
    def value(self):
        """Returns the value of the amount"""
        return self._value

    def __add__(self, other):
        other = Amount(other)
        return Amount(self.value + other.value)

    def __sub__(self, other):
        other = Amount(other)
        return Amount(self.value - other.value)

    def __mul__(self, other):
        other = Amount(other)
        return Amount(self.value * other.value)

    def __truediv__(self, other):
        other = Amount(other)
        return Amount(self.value / other.value)

    def __floordiv__(self, other):
        other = Amount(other)
        return Amount(self.value // other.value)

    def __mod__(self, other):
        other = Amount(other)
        return Amount(self.value % other.value)

    def __pow__(self, other):
        other = Amount(other)
        return Amount(self.value ** other.value)

    def __lt__(self, other):
        other = Amount(other)
        return self.value < other.value

    def __le__(self, other):
        other = Amount(other)
        return self.value <= other.value

    def __eq__(self, other):
        other = Amount(other)
        return self.value == other.value

    def __ne__(self, other):
        other = Amount(other)
        return self.value != other.value

    def __gt__(self, other):
        other = Amount(other)
        return self.value > other.value

    def __ge__(self, other):
        other = Amount(other)
        return self.value >= other.value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"Amount({self.value})"
