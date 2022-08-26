import components.constants as cst
from components.hand import Combo


class Player:
    """"""
    def __init__(self, name: str = None, seat: int = None, stack: float = None):
        self._name = name
        self._seat = seat
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
        #self.combos_range = CombosRange()

    def __str__(self):
        return f"Name: {self.name}\nSeat: {self.seat}\nStack: {self.stack}\nHero: {self.is_hero}\nCombo: {self.combo}"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        if len(name) > 12:
            raise ValueError
        else:
            self._name = name

    @property
    def seat(self):
        try:
            return self._seat
        except AttributeError:
            return None

    @seat.setter
    def seat(self, seat: int):
        if seat < 0 or seat > 10:
            raise ValueError
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
        self._combo = combo

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position

    @property
    def is_all_in(self):
        return self.stack == 0

    def fold(self):
        self.folded = True

    def reset(self):
        self.folded = False

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