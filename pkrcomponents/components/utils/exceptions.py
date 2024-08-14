"""This module gathers all custom exceptions used in the project"""


class NotSufficientBetError(Exception):
    """Raised when the bet is not sufficient to cover the minimum bet"""
    def __init__(self, value, player):
        message = (f"Bet value must be at least {player.table.min_bet} or player should go all-in.\n"
                   f"Current street: {player.table.street}\n"
                   f"Stack: {player.stack}\n"
                   f"Bet Value: {value}\n")
        self.message = message
        super().__init__(self.message)


class NotSufficientRaiseError(Exception):
    """Raised when the raise is not sufficient to cover the bet"""
    def __init__(self, value, player):
        total_value = player.to_call + value
        message = (f"Raise value must be at least {player.min_raise} or player should go all-in.\n"
                   f"Value to call: {player.to_call}\n"
                   f"Minimum bet: {player.table.min_bet}\n"
                   f"Highest bet in this street: {player.table.pot.highest_bet}\n"
                   f"Stack: {player.stack}\n"
                   f"Player's current bet: {player.current_bet}\n"
                   f"Player's Min Raise: {player.min_raise}\n"
                   f"Raise Total Bet Value: {total_value}\n"
                   f"Raise Value: {value}\n"
                   f"Raise value must be at least {player.min_raise} or player should go all-in.\n")
        self.message = message
        super().__init__(self.message)


class HandEndedError(Exception):
    """Raised when trying to make an action after the hand has ended"""
    def __init__(self, message="The hand has ended. No more actions can be made."):
        self.message = message
        super().__init__(self.message)


class ShowdownNotReachedError(Exception):
    """Raised when trying to show a combo hand before the showdown"""
    def __init__(self, message="Error converting showdown data: Showdown not reached"):
        self.message = message
        super().__init__(self.message)


class CannotParseWinnersError(Exception):
    """Raised when trying to parse the winners of a hand"""
    def __init__(self, message="Cannot parse the winners of the hand"):
        self.message = message
        super().__init__(self.message)


class EmptyButtonSeatError(Exception):
    """Raised when the button seat is not a valid seat"""
    def __init__(self, message="The button seat is not a valid seat"):
        self.message = message
        super().__init__(self.message)


class SeatTakenError(Exception):
    def __init__(self):
        self.message = "Seat already taken"
        super().__init__(self.message)


class FullTableError(Exception):
    def __init__(self):
        self.message = "Table is full"
        super().__init__(self.message)


class BoardNotEmptyError(Exception):
    def __init__(self):
        self.message = "Board is not empty"
        super().__init__(self.message)


class PlayerAlreadyFoldedError(Exception):
    def __init__(self):
        self.message = "Player has already folded"
        super().__init__(self.message)


class PlayerNotOnTableError(Exception):
    def __init__(self, name_item):
        self.message = f"Player {name_item} is not on the table"
        super().__init__(self.message)
