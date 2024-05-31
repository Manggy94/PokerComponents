from pkrcomponents.constants import Position, Street


def convert_to_position(value: (str, Position)) -> Position:
    return Position(value.upper()) if isinstance(value, str) else value

def convert_to_street(value: (str, Street)) -> Street:
    return Street(value) if isinstance(value, str) else value
