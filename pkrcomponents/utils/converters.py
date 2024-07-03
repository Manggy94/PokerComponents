from pkrcomponents.actions.street import Street
from pkrcomponents.cards.card import Card
from pkrcomponents.players.position import Position
from pkrcomponents.tournaments.speed import TourSpeed


def convert_to_position(value: (str, Position)) -> Position:
    return Position(value.upper()) if isinstance(value, str) else value


def convert_to_street(value: (str, Street)) -> Street:
    return Street(value) if isinstance(value, str) else value


def convert_to_speed(value: (str, TourSpeed, None)) -> TourSpeed:
    if isinstance(value, str):
        return TourSpeed(value)
    elif isinstance(value, TourSpeed):
        return value
    else:
        return TourSpeed.REGULAR


def convert_to_card(value: (str, Card, None)) -> (Card, None):
    if isinstance(value, str):
        return Card(value)
    elif isinstance(value, Card):
        return value
    else:
        return None
