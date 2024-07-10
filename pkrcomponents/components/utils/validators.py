def validate_players_remaining(instance, attribute, value):
    if not isinstance(value, int):
        raise TypeError(f"{attribute.name} must be an int")
    if value < 1:
        raise ValueError(f"{attribute.name} must be at least 1")
    if value > instance.total_players:
        raise ValueError(f"{attribute.name} cannot be greater than total_players")


