from pkrcomponents.hand import Combo
from pkrcomponents.constants import Position


def convert_to_combo(value: str) -> Combo:
    return Combo(f"{value}")


def convert_to_position(value: (str, Position)) -> Position:
    return Position(value.upper()) if isinstance(value, str) else value
