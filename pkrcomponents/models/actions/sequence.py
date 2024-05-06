from .move import Move


class Sequence:
    """
    A model to describe poker action sequences
    """
    symbol: str
    moves: list[Move]

    def __init__(self, symbol, moves):
        self.symbol = symbol
        self.moves = moves
