from pkrcomponents.components.utils.common import PokerEnum


class BlindType(PokerEnum):
    """Class describing the blind type"""
    SMALL_BLIND = "SB", "Small blind", "small blind"
    BIG_BLIND = "BB", "Big blind", "big blind"
    ANTE = "A", "Ante", "ante"

    @property
    def name(self):
        """
        Returns:
            (str): The name of the action
        """
        return self._name_

    @property
    def symbol(self):
        """
        Returns:
            (str): The symbol of the action
        """
        return self._value_[0]
