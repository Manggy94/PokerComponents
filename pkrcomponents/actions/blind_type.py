from pkrcomponents.utils.common import PokerEnum


class BlindType(PokerEnum):
    """Class describing the blind type"""
    SMALL_BLIND = "SB", "Small blind", "small blind"
    BIG_BLIND = "BB", "Big blind", "big blind"
    ANTE = "A", "Ante", "ante"

    @property
    def name(self):
        return self._name_

    @property
    def symbol(self):
        return self._value_[0]
