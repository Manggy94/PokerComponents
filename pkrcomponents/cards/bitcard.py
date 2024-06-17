from __future__ import annotations
from pkrcomponents.cards.card import Card
from pkrcomponents.cards.rank import Rank
from pkrcomponents.cards.suit import Suit
import math


class BitCard(int):
    """
        Class converting a card into an integer for fast poker evaluation, inspired by Will Drevo
        Card objects are transformed into native Python 32-bit integers.
        Most of the bits are used, and have a specific meaning. See below:
        .. table:: Card
            :align: center
            :widths: auto
            ========  ========  ========  ========
            xxxbbbbb  bbbbbbbb  shdcrrrr  xxpppppp
            ========  ========  ========  ========
        - p = prime number of rank (in binary) (deuce=2, trey=3, four=5, ..., ace=41), on 6 bits [0-63]
        - r = rank of card (in binary) (deuce=0, trey=1, four=2, five=3, ..., ace=12), on 4 bits [0-15]
        - cdhs = suit of card (bit turned on based on suit of card)
        - b = bit turned on depending on rank of card (deuce=1st bit, trey=2nd bit, ...)
        - x = unused
        **Example**
            .. table::
                :align: center
                :widths: auto
                ================ ========  ========  ========  ========
                Card             xxxAKQJT  98765432  SHDCrrrr  xxPPPPPP
                ================ ========  ========  ========  ========
                King of Diamonds 00001000  00000000  00101011  00100101
                Five of Spades   00000000  00001000  10000011  00000111
                Jack of Clubs    00000010  00000000  00011001  00011101
                ================ ========  ========  ========  ========
         This representation allows for minimal memory overhead along with fast applications
        necessary for poker:
            - Make a unique prime product for each hand (by multiplying the prime bits)
            - Detect flushes (bitwise && for the suits)
            - Detect straights (shift and bitwise &&)

        """
    ranks = tuple(f"{x}" for x in list(Rank))
    int_ranks = tuple(range(13))
    primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)
    suits = tuple(f"{x}" for x in list(Suit))
    int_suits = tuple(2 ** n for n in range(4))
    char_to_int_rank = dict(zip(ranks, int_ranks))
    char_to_int_suit = dict(zip(suits, int_suits))
    int_to_char_suit = "xcdxsxxxh"

    def __new__(cls, card) -> BitCard:
        if isinstance(card, str):
            return BitCard.from_string(card)
        elif isinstance(card, Card):
            return BitCard.from_card(card)
        return BitCard.from_int(card)

    @classmethod
    def from_card(cls, card: Card) -> BitCard:
        """
        Converts Card to binary integer representation of card
        """
        rank_int = BitCard.char_to_int_rank[f"{card.rank}"]
        suit_int = BitCard.char_to_int_suit[f"{Card(card).suit}"]
        prime = BitCard.primes[rank_int]
        bit_rank = 1 << rank_int << 16
        rank = rank_int << 8
        suit = suit_int << 12
        card_int = bit_rank | suit | rank | prime
        return BitCard.from_int(card_int)

    @classmethod
    def from_string(cls, str_card) -> BitCard:
        """
        Converts a string representation of a card to a 32-bit integer representation
        Example:
            "Kd" --> 134236965
        Args:
            str_card (str): A string representation of a card
        Returns:
            BitCard: The 32-bit int representing the card as described above
        """
        card = Card(str_card)
        return BitCard.from_card(card)

    @classmethod
    def from_int(cls, card_int: int) -> BitCard:
        """
        Converts an already well-formed card integer as described above
        Example:
            134236965 --> Card("Kd")
        Args:
            card_int (int): An int representing a card.
        Returns:
            Card: The 32-bit int representing the card as described above
        """
        return super(BitCard, cls).__new__(cls, card_int)

    @property
    def rank(self) -> int:
        """
        The rank of the card as an int.
        Example:
            134236965 ("Kd") --> 11
            268440327 ("As") --> 12
        Returns:
            int: Number between 0-12, representing the rank of the card.
        """

        return (self >> 8) & 0xF

    @property
    def suit(self) -> int:
        """
        The suit int of the card using the following table:
        .. table::
            :align: center
            :widths: auto
            ========  ======
            Suit      Number
            ========  ======
            Spades      1
            Hearts      2
            Diamonds    4
            Clubs       8
            ========  ======
        Example:
            134236965 ("Kd") --> 2
        Returns:
            int: 1,2,4, or 8, representing the suit of the card from the above table.
        """
        return (self >> 12) & 0xF

    @property
    def bitrank(self) -> int:
        """
        The bitrank of the card. This returns 2^k where k is the
        rank of the card.
        Example:
            134236965 ("Kd") --> 2^11
        Returns:
            int: 2^k where k is the rank of the card.
        """
        return (self >> 16) & 0x1FFF

    @property
    def prime(self) -> int:
        """
        The prime associated with the card. This returns the kth prime
        starting at 2 where k is the rank of the card.
        Example:
            134236965 ("Kd") --> 37
        """
        return self & 0x3F

    @property
    def binary_string(self) -> str:
        """
        For debugging purposes. Displays the binary number as a
         string in groups of four digits, readable by a human.
        """
        bin_str = bin(self)[2:][::-1]  # chop off the 0b and THEN reverse string
        output = list("".join(["0000" + "\t"] * 7) + "0000")

        for i, b_char in enumerate(bin_str, 0):
            output[i + int(i / 4)] = b_char

        # output the string to console
        output.reverse()
        return "".join(output)

    @classmethod
    def cards_to_int(cls, cards):
        return [BitCard(card) for card in cards]

    @classmethod
    def prime_product_from_cards(cls, cards):
        return math.prod(BitCard(card).prime for card in cards)

    @classmethod
    def prime_product_from_rankbits(cls, rankbits: int) -> int:
        """
        Returns the prime product using the bitrank (b)
        bits of the hand. Each 1 in the sequence is converted
        to the correct prime and multiplied in.
        Primarily used to evaluate flushes and straights,
        two occasions where we know the ranks are *ALL* different.
        Assumes that the input is in form (set bits):
        .. table::
                :align: center
                :widths: auto
                ========  ========
                xxxbbbbb  bbbbbbbb
                ========  ========
        Args:
            rankbits (int): a single 32-bit (only 13-bits set) integer representing
                the ranks of 5 *different* ranked card (5 of 13 bits are set)
        Returns:
            int: The product of all primes in the hand, corresponding
                to the rank of the card.
        """
        product = 1
        for i in BitCard.int_ranks:
            # if the ith bit is set
            if rankbits & (1 << i):
                product *= BitCard.primes[i]
        return product
