from pkrcomponents.actions.street import Street
from pkrcomponents.players.position import Position
from pkrcomponents.cards.card import Card


def convert_to_position(value: (str, Position)) -> Position:
    return Position(value.upper()) if isinstance(value, str) else value


def convert_to_street(value: (str, Street)) -> Street:
    return Street(value) if isinstance(value, str) else value


def convert_to_card(value: (str, Card, None)) -> (Card, None):
    if isinstance(value, str):
        return Card(value)
    elif isinstance(value, Card):
        return value
    else:
        return None
