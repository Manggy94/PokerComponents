from pkrcomponents.constants import Position, Street
from pkrcomponents.card import Card


def convert_to_position(value: (str, Position)) -> Position:
    return Position(value.upper()) if isinstance(value, str) else value


def convert_to_street(value: (str, Street)) -> Street:
    return Street(value) if isinstance(value, str) else value


def convert_to_card(value: (str, Card, None)) -> Card:
    return Card(value) if isinstance(value, str) else value if isinstance(value, Card) else None
