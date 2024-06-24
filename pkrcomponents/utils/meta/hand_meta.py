from pkrcomponents.cards.rank import Rank


class HandMeta(type):
    """Makes Hand class iterable. __iter__ goes through all hands in ascending order."""

    def __new__(mcs, clsname, bases, classdict):
        """Cache all possible Hand instances on the class itself."""
        cls = super(HandMeta, mcs).__new__(mcs, clsname, bases, classdict)
        cls.all_hands = tuple(cls.get_non_paired_hands()) + tuple(cls.get_paired_hands())
        return cls

    def get_non_paired_hands(cls):
        """Generator of all non-paired hands"""
        for rank1 in Rank:
            for rank2 in (rk for rk in Rank if rk < rank1):
                yield cls(f"{rank1}{rank2}o")
                yield cls(f"{rank1}{rank2}s")

    def get_paired_hands(cls):
        """Generator of all paired hands"""
        for rank in Rank:
            yield cls(rank.val * 2)

    def get_suited_hands(cls):
        """Generator of all suited hands"""
        for rank1 in Rank:
            for rank2 in (rk for rk in Rank if rk < rank1):
                yield cls(f"{rank1}{rank2}s")

    def get_offsuit_hands(cls):
        """Generator of all offsuit hands"""
        for rank1 in Rank:
            for rank2 in (rk for rk in Rank if rk < rank1):
                yield cls(f"{rank1}{rank2}o")

    def __iter__(cls):
        return iter(cls.all_hands)

    def __len__(cls):
        return len(cls.all_hands)
