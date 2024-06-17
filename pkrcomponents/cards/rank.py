from pkrcomponents.utils.common import PokerEnum


class Rank(PokerEnum):
    """
    Rank of a card in a deck, from 2 to Ace.

    Methods:
        difference: tells the numerical difference between two ranks
    """
    DEUCE = "2", 2
    THREE = "3", 3
    FOUR = "4", 4
    FIVE = "5", 5
    SIX = "6", 6
    SEVEN = "7", 7
    EIGHT = "8", 8
    NINE = "9", 9
    TEN = "T", 10
    JACK = "J", 11
    QUEEN = "Q", 12
    KING = "K", 13
    ACE = "A", 1

    @property
    def symbol(self):
        return self.value[0]

    def __str__(self):
        return self.symbol

    @property
    def name(self):
        return self._name_

    @property
    def short_name(self):
        return self.symbol

    @property
    def is_broadway(self):
        return self in BROADWAY_RANKS

    @property
    def is_face(self):
        return self in FACE_RANKS

    @classmethod
    def difference(cls, first, second) -> int:
        """
        Tells the numerical difference between two ranks.

        Args:
            first (Rank): the first rank
            second (Rank): the second rank

        Returns:
            int: the difference between the two ranks
        """

        # so we always get a Rank instance even if string were passed in
        first, second = cls(first), cls(second)
        rank_list = list(cls)
        a = rank_list.index(first)+2
        b = rank_list.index(second)+2
        if a == 14:
            return min(abs(a-b), abs(1-b))
        elif b == 14:
            return min(abs(a - b), abs(a - 1))
        return abs(rank_list.index(first) - rank_list.index(second))

    def __sub__(self, other):
        return self.difference(self, other)


FACE_RANKS = Rank("J"), Rank("Q"), Rank("K")
BROADWAY_RANKS = Rank("T"), Rank("J"), Rank("Q"), Rank("K"), Rank("A")
