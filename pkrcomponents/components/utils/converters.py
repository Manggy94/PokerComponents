import re
from pkrcomponents.components.actions.street import Street
from pkrcomponents.components.cards import Card
from pkrcomponents.components.players.position import Position
from pkrcomponents.components.tournaments.speed import TourSpeed


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




def pascal_to_snake_case(pascal_str):
    snake_str = re.sub(r'(?<!^)(?=[A-Z])', '_', pascal_str)
    return snake_str.lower()
