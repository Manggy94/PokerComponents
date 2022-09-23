from components.listings import players_positions


class Players:
    """"""
    _BB: int
    pl_list: list
    name_dict: dict
    seat_dict: dict
    positions_mapper: dict

    def __init__(self):
        self.pl_list = []
        self.name_dict = {}
        self.seat_dict = {}

    def __getitem__(self, item):
        if type(item) == str:
            return self.name_dict[item]
        elif type(item) == int:
            return self.seat_dict[item]
        else:
            raise ValueError("To get a player, call it by its name or seat")

    def __len__(self):
        return len(self.occupied_seats)

    def __contains__(self, item):
        return self.pl_list.__contains__(item)

    def __iter__(self):
        return self.pl_list.__iter__()

    @property
    def len(self):
        return self.__len__()

    @property
    def occupied_seats(self):
        tab = list(self.seat_dict.keys())
        tab.sort()
        return tab

    @property
    def bb(self):
        return self._BB

    @bb.setter
    def bb(self, seat):
        if seat in self.occupied_seats:
            self._BB = seat
        else:
            self._BB = self.occupied_seats[0]

    @property
    def preflop_ordered_seats(self):
        cut = self.occupied_seats.index(self.bb) + 1
        return self.occupied_seats[cut:] + self.occupied_seats[:cut]

    @property
    def positions_mapper(self):
        nb_players = self.len
        positions = players_positions[nb_players]
        return dict(zip(self.preflop_ordered_seats, positions))

    def distribute_positions(self):
        for seat, pos in self.positions_mapper.items():
            pl = self.seat_dict[seat]
            pl.position = pos

    @property
    def postflop_ordered_seats(self):
        return self.preflop_ordered_seats[-2:] + self.preflop_ordered_seats[:-2]
