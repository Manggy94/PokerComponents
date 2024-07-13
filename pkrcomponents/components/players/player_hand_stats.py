from attrs import define, Factory, field
from attrs.validators import instance_of
import csv
from pkrcomponents.components.players.street_hand_stats import preflop, postflop, general
from pkrcomponents.components.players.street_hand_stats.base import StreetHandStatsBase


@define
class PlayerHandStats(StreetHandStatsBase):
    """
    This class represents the statistics of a player's hand in a poker game

    Methods:
        reset: Resets all stats
    """
    # A. Preflop stats
    preflop = field(
        default=Factory(preflop.PreflopPlayerHandStats),
        metadata={'description': 'Preflop player stats for a hand'},
        validator=instance_of(preflop.PreflopPlayerHandStats))
    flop = field(
        default=Factory(postflop.PostflopPlayerHandStats),
        metadata={'description': 'Flop player stats for a hand'},
        validator=instance_of(postflop.PostflopPlayerHandStats))
    turn = field(
        default=Factory(postflop.PostflopPlayerHandStats),
        metadata={'description': 'Turn player stats for a hand'},
        validator=instance_of(postflop.PostflopPlayerHandStats))
    river = field(
        default=Factory(postflop.PostflopPlayerHandStats),
        metadata={'description': 'River player stats for a hand'},
        validator=instance_of(postflop.PostflopPlayerHandStats))
    general = field(
        default=Factory(general.GeneralPlayerHandStats),
        metadata={'description': 'General player stats for a hand'},
        validator=instance_of(general.GeneralPlayerHandStats))

    def __attrs_post_init__(self):
        self.preflop.reset()
        self.flop.reset()
        self.turn.reset()
        self.river.reset()
        self.general.reset()



if __name__ == '__main__':
    PlayerHandStats.generate_description_file()
