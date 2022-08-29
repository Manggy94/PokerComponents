import components.constants as cst
from components.hand import Combo


class Player:
    """"""

    _name: str
    _seat: int
    _stack: float
    init_stack: float
    _combo: Combo or None
    folded: bool
    _hero: bool
    _position: cst.Position or None

    def __init__(self, name: str = "Villain", seat=0, stack: float = 0):
        self.name = name
        self.seat = seat
        if stack < 0:
            raise ValueError("Init stack cannot be negative")
        else:
            self._stack = stack
            self.init_stack = stack
        self._combo = None
        self.folded = False
        self._hero = False
        self.current_bet = 0
        self._position = None
        self.actions = {
            f"{cst.Street('Preflop')}": [],
            f"{cst.Street('Flop')}": [],
            f"{cst.Street('Turn')}": [],
            f"{cst.Street('River')}": []
        }
        self.played = False

    def __str__(self):
        return f"Name: {self.name}\nSeat: {self.seat}\nStack: {self.stack}\nHero: {self.is_hero}\nCombo: {self.combo}"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        if len(name) > 12:
            raise ValueError("Player name length should be between 3 and 12 characters")
        else:
            self._name = name

    @property
    def seat(self):
        try:
            return self._seat
        except AttributeError:
            return None

    @seat.setter
    def seat(self, seat):
        if seat < 0 or seat > 10 or type(seat) != int:
            raise ValueError("Seat should be an int between 0 and 10")
        else:
            self._seat = seat

    @property
    def stack(self):
        return self._stack

    @stack.setter
    def stack(self, stack):
        if stack < 0:
            self._stack = 0
        else:
            self._stack = stack

    @property
    def combo(self):
        return self._combo

    @combo.setter
    def combo(self, combo: Combo):
        combo = Combo(combo)
        self._combo = combo

    @property
    def has_combo(self) -> bool:
        return self._combo is not None

    @property
    def is_hero(self) -> bool:
        return self._hero

    @is_hero.setter
    def is_hero(self, is_hero):
        self._hero = is_hero

    def shows(self, combo):
        self.combo = combo

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        position = cst.Position(position)
        self._position = position

    @property
    def is_all_in(self):
        return self.stack == 0

    def fold(self):
        self.folded = True
        self.played = True

    def reset(self):
        self.folded = False
        self.played = False

    def reset_street_status(self):
        self.played = False

    def to_call(self, table):
        return table.highest_bet-self.current_bet

    def can_play(self, table):
        return not (self.is_all_in or (self.to_call(table) == 0 and self.played))

    def pot_odds(self, table):
        to_call = self.to_call(table)
        if to_call != 0:
            pot_odds = table.pot/to_call
        else:
            pot_odds = float("inf")
        return pot_odds

    def req_equity(self, table):
        return 1/(1+self.pot_odds(table))


class Players:
    """"""
    preflop_starter = "BB"
    postflop_starter = "BTN"

    def __init__(self):
        self.pl_list = []
        self.name_dict = {}
        self.seat_dict = {}
        self.positions = {}

    def append(self, player):
        if type(player) != Player:
            raise ValueError("Only Players can be added to Players")
        self.pl_list.append(player)
        self.name_dict[player.name] = player
        self.seat_dict[player.seat] = player

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