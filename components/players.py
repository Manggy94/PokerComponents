from components.listings import players_positions


class Players:
    """
    Class representing many players on a table
    """
    _BB: int
    _pl_list: list
    _name_dict: dict
    _seat_dict: dict
    _positions_mapper: dict

    def __init__(self):
        self.pl_list = []
        self.name_dict = {}
        self.seat_dict = {}
        self._BB = 1

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
    def pl_list(self):
        """List of all the players on the table in appearance order"""
        return self._pl_list

    @pl_list.setter
    def pl_list(self, listing):
        """Setter for players list property"""
        self._pl_list = listing

    @property
    def name_dict(self):
        """A dict {name: player}"""
        return self._name_dict

    @name_dict.setter
    def name_dict(self, dico):
        """Setter for name dict property"""
        self._name_dict = dico

    @property
    def seat_dict(self):
        """A dict {seat: player}"""
        return self._seat_dict

    @seat_dict.setter
    def seat_dict(self, dico):
        """Setter for seat dict property"""
        self._seat_dict = dico

    @property
    def len(self):
        """Returns the number of players on the table"""
        return self.__len__()

    @property
    def occupied_seats(self):
        """returns an ordered list of the number of every occupied seat on the table"""
        tab = list(self.seat_dict.keys())
        tab.sort()
        return tab

    @property
    def bb(self):
        """Returns the seat of table's Big Blind"""
        return self._BB

    @bb.setter
    def bb(self, seat):
        """ Setter for bb property"""
        if seat in self.occupied_seats:
            self._BB = seat
        else:
            self._BB = self.occupied_seats[0]

    @property
    def preflop_ordered_seats(self):
        """Returns the list of the indexes of players on the table, with preflop playing order"""
        cut = self.occupied_seats.index(self.bb) + 1
        return self.occupied_seats[cut:] + self.occupied_seats[:cut]

    @property
    def positions_mapper(self):
        """Returns a dict {seat: position} """
        nb_players = self.len
        positions = players_positions[nb_players]
        return dict(zip(self.preflop_ordered_seats, positions))

    @property
    def seats_mapper(self):
        """Returns a dict {position: seat} """
        nb_players = self.len
        positions = tuple(f"{pos}" for pos in players_positions[nb_players])
        return dict(zip(positions, self.preflop_ordered_seats))

    def distribute_positions(self):
        """When  players are on the table and bb is set, distributes a position to each player on the table"""
        for seat, pos in self.positions_mapper.items():
            pl = self.seat_dict[seat]
            pl.position = pos

    @property
    def postflop_ordered_seats(self):
        """Returns the list of the indexes of players on the table, with postflop playing order"""
        return self.preflop_ordered_seats[-2:] + self.preflop_ordered_seats[:-2]
