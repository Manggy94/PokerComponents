import itertools
from pkrcomponents.cards.bitcard import BitCard
from pkrcomponents.cards.lookup_table import LookupTable

LOOKUP_TABLE = LookupTable()


class Evaluator:
    """Evaluates hand strengths with optimizations in terms of speed and memory usage."""

    @classmethod
    def _five(cls, cards) -> int:
        """
        Performs an evaluation given card in integer form, mapping them to
        a rank in the range [1, 7462], with lower ranks being more powerful.
        Variant of Cactus Kev's 5 card evaluator.

        """
        (card_0, card_1, card_2, card_3, card_4) = tuple(BitCard(cards[i]) for i in range(5))
        # if flush
        if card_0 & card_1 & card_2 & card_3 & card_4 & 0xF000:
            hand_or = (card_0 | card_1 | card_2 | card_3 | card_4) >> 16
            prime = BitCard.prime_product_from_rankbits(hand_or)
            return LOOKUP_TABLE.flush_lookup[prime]

        # otherwise
        prime = BitCard.prime_product_from_cards(cards)
        return LOOKUP_TABLE.unsuited_lookup[prime]

    @classmethod
    def evaluate(cls, cards, board) -> int:
        """
        Evaluates the best five-card hand from the given cards and board. Returns
        the corresponding rank.
        """
        all_cards = cards + board
        return min(cls._five(hand) for hand in itertools.combinations(all_cards, 5))

    @classmethod
    def get_rank_class(cls, hand_rank: int) -> int:
        """
        Returns the class of hand given the hand hand_rank returned from evaluate from
        9 rank classes.

        Example:
            straight flush is class 1, high card is class 9, full house is class 3.

        Returns:
            int: A rank class int describing the general category of hand from 9 rank classes.
                Example, straight flush is class 1, high card is class 9, full house is class 3.

        """
        max_rank = min(rank for rank in LOOKUP_TABLE.MAX_TO_RANK_CLASS if hand_rank <= rank)
        return LOOKUP_TABLE.MAX_TO_RANK_CLASS[max_rank]

    @classmethod
    def score_to_string(cls, hand_rank: int) -> str:
        """
        Returns a string describing the hand of the hand_rank.

        Example:
            166 -> "Four of a Kind"

        Args:
            hand_rank (int): The rank of the hand given by :meth:`evaluate`
        Returns:
            string: A human-readable string of the hand rank (i.e. Flush, Ace High).

        """
        return LOOKUP_TABLE.RANK_CLASS_TO_STRING[cls.get_rank_class(hand_rank)]

    @classmethod
    def get_five_card_rank_percentage(cls, hand_rank: int) -> float:
        """
        The percentage of how many of the 7462 hand strengths are worse than the given one.

        Args:
            hand_rank (int): The rank of the hand given by :meth:`evaluate`
        Returns:
            float: The percentile strength of the given hand_rank (i.e. what percent of hands is worse
                than the given one).

        """
        return 1 - float(hand_rank) / float(LOOKUP_TABLE.MAX_HIGH_CARD)
