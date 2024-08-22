import csv
import pandas as pd

from attrs import define, Factory, field
from attrs.validators import instance_of
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

    def to_dataframe(self) -> pd.DataFrame:
        """
        Converts the object to a pandas DataFrame
        """
        street_names = ['general', 'preflop', 'flop', 'turn', 'river']
        data_frames = [getattr(self, street_name).to_dataframe() for street_name in street_names]
        # Join all dataframes with the usage of street_names as keys
        df = pd.concat(data_frames, axis=1, keys=street_names)
        # Modify the column names by adding the street name as prefix to the current column names
        df.columns = [f'{street_name}_{column_name}' for street_name, column_name in df.columns]
        return df



if __name__ == '__main__':
    PlayerHandStats.generate_description_file()
