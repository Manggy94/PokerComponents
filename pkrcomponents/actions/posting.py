from attrs import define, field
from attrs.validators import instance_of, ge

from pkrcomponents.actions.blind_type import BlindType


@define
class Posting:
    """
    This class represents a posting made by a player in a poker game

    Attributes:
        player_name(TablePlayer): The name of player making the posting
        blind(BlindType): The blind type of the posting
        value(float): The value of the posting made by the player

    Methods:
        __str__(): Returns a string representation of the posting
        execute(): Executes the posting

    """

    player_name = field(validator=[instance_of(str)])
    blind = field(default=BlindType.BIG_BLIND, validator=[instance_of(BlindType)], converter=BlindType)
    value = field(default=0, validator=[ge(0), instance_of(float)], converter=float)

    def execute(self, player):
        """
        Executes the posting
        """
        player.pay(self.value)
        player.table.pot.update_highest_bet(player.current_bet)
        player.table.postings.append(self)


class AntePosting(Posting):
    """
    This class represents an ante posting made by a player in a poker game
    """
    def __init__(self, player_name, value):
        super().__init__(player_name=player_name, blind=BlindType.ANTE, value=value)


class BlindPosting(Posting):
    """
    This class represents a blind posting made by a player in a poker game
    """

    def update_current_bet(self, player):
        player.current_bet += self.value

    def execute(self, player):
        """
        Executes the posting
        """
        self.update_current_bet(player)
        super().execute(player)


class SBPosting(BlindPosting):
    """
    This class represents a Small Blind posting made by a player in a poker game
    """
    def __init__(self, player_name, value):
        super().__init__(player_name=player_name, blind=BlindType.SMALL_BLIND, value=value)


class BBPosting(BlindPosting):
    """
    This class represents a Big Blind posting made by a player in a poker game
    """
    def __init__(self, player_name, value):
        super().__init__(player_name=player_name, blind=BlindType.BIG_BLIND, value=value)

    def execute(self, player):
        """
        Executes the posting
        """
        super().execute(player)
        player.table.min_bet = player.table.level.bb*2
        player.table.cnt_bets += 1