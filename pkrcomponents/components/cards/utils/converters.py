from pkrcomponents.components.cards import Card


def convert_to_card(value: (str, Card, None)) -> (Card, None):
    if isinstance(value, str):
        return Card(value)
    elif isinstance(value, Card):
        return value
    else:
        return None