#   from components.table_player import TablePlayer


class Players:
    """"""
    preflop_starter = "BB"
    postflop_starter = "BTN"

    def __init__(self):
        self.pl_list = []
        self.name_dict = {}
        self.seat_dict = {}
        self.positions = {}

    def __getitem__(self, item):
        try:
            if type(item) == str:
                return self.name_dict[item]
            elif type(item) == int:
                return self.seat_dict[item]
        except KeyError:
            raise KeyError

    def __len__(self):
        return self.name_dict.__len__()

    def __contains__(self, item):
        return self.pl_list.__contains__(item)

    def __iter__(self):
        return self.pl_list.__iter__()

    def find(self, name: str):
        try:
            return self.name_dict[name]
        except KeyError:
            print(f"{name} is not currently on this table")
