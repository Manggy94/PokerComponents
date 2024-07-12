from attrs import define, Factory, field
from attrs.validators import instance_of
import csv
#from pkrcomponents.components.players.datafields import preflop, flop, turn, river, general
from pkrcomponents.components.players.street_hand_stats import preflop, postflop, general


@define
class HandStats:
    """
    This class represents the statistics of a player's hand in a poker game

    Methods:
        reset: Resets all stats
    """
    # A. Preflop stats
    preflop = field(
        default=Factory(preflop.PreflopPlayerHandStats),
        metadata={'description': 'Preflop stats'},
        validator=instance_of(preflop.PreflopPlayerHandStats))
    flop = field(
        default=Factory(postflop.PostflopPlayerHandStats),
        metadata={'description': 'Flop stats'},
        validator=instance_of(postflop.PostflopPlayerHandStats))
    turn = field(
        default=Factory(postflop.PostflopPlayerHandStats),
        metadata={'description': 'Turn stats'},
        validator=instance_of(postflop.PostflopPlayerHandStats))
    river = field(
        default=Factory(postflop.PostflopPlayerHandStats),
        metadata={'description': 'River stats'},
        validator=instance_of(postflop.PostflopPlayerHandStats))
    general = field(
        default=Factory(general.GeneralPlayerHandStats),
        metadata={'description': 'General stats'},
        validator=instance_of(general.GeneralPlayerHandStats))

    def __attrs_post_init__(self):
        self.preflop.reset()
        self.flop.reset()
        self.turn.reset()
        self.river.reset()
        self.general.reset()

    def reset(self):
        """
        Resets the statistics
        """
        for attribute in self.__attrs_attrs__:
            if not isinstance(attribute.default, Factory):
                setattr(self, attribute.name, attribute.default)
            else:
                setattr(self, attribute.name, attribute.default.factory())

#     @classmethod
#     def generate_description_file(cls):
#         """
#         Generate a csv file to describe data from class
#         """
#         with open('hand_stats_description.csv', 'w', newline='') as csvfile:
#             fieldnames = ['name', 'default', 'description', 'type']
#             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#
#             writer.writeheader()
#             for attribute in cls.__attrs_attrs__:
#                 row = {
#                     'name': attribute.name,
#                     'default': attribute.default if not isinstance(attribute.default, Factory)
#                     else attribute.default.factory(),
#                     'description': attribute.metadata.get('description', 'No description'),
#                     'type': attribute.metadata.get('type', 'No type')
#                 }
#                 writer.writerow(row)
#         print("CSV file 'class_description.csv' generated successfully.")
#
#
# if __name__ == '__main__':
#     HandStats.generate_description_file()
