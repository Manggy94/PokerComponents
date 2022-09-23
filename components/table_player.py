from components.constants import Position, Street
from components.hand import Combo
from components.table import Table


class TablePlayer:
    """"""

    _name: str
    _seat: int
    _stack: float
    init_stack: float
    _combo: Combo or None
    folded: bool
    _hero: bool
    _position: Position or None
    _table: Table

    def __init__(self, name: str = "Villain", seat=0, stack: float = 0):
        self.name = name
        self.seat = seat
        if stack < 0:
            raise ValueError("Init stack cannot be negative")
        else:
            self._stack = stack
            self._init_stack = stack
        self._combo = None
        self.folded = False
        self._hero = False
        self.current_bet = 0
        self._position = None
        self.actions = {
            f"{Street('Preflop')}": [],
            f"{Street('Flop')}": [],
            f"{Street('Turn')}": [],
            f"{Street('River')}": []
        }
        self.played = False

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
        return self._seat

    @seat.setter
    def seat(self, seat):
        if seat not in range(11):
            raise ValueError("Seat should be an int between 0 and 10")
        else:
            self._seat = seat

    @property
    def stack(self):
        return self._stack

    @stack.setter
    def stack(self, stack):
        self._stack = max(0.0, float(stack))

    @property
    def init_stack(self):
        return self._init_stack

    @init_stack.setter
    def init_stack(self, stack):
        self._init_stack = max(0.0, float(stack))
        self.stack = self.init_stack

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
        position = Position(position)
        self._position = position

    def distribute(self, combo):
        combo = Combo(combo)
        self.table.deck.draw(combo.first)
        self.table.deck.draw(combo.second)
        self.combo = combo

    def fold(self):
        self.folded = True
        self.played = True

    def reset(self):
        self.folded = False
        self.played = False

    def reset_street_status(self):
        self.played = False

    @property
    def to_call(self):
        return min(self.table.current_pot.highest_bet-self.current_bet, self.stack)

    @property
    def is_all_in(self):
        return self.stack == 0

    @property
    def can_play(self):
        return not (self.is_all_in or (self.to_call == 0 and self.played))

    @property
    def pot_odds(self) -> float:
        to_call = self.to_call
        if to_call != 0:
            pot_odds = float(self.table.pot/to_call)
        else:
            pot_odds = float("inf")
        return pot_odds

    @property
    def req_equity(self):
        return 1.0/(1.0+self.pot_odds)

    @property
    def table(self):
        return self._table

    def sit(self, table):
        self._table = table
        self.table.players.pl_list.append(self)
        self.table.players.name_dict[self.name] = self
        self.table.players.seat_dict[self.seat] = self
        self.reset()

    def pay(self, value):
        print(self.table.current_pot.max_bet)
        amount = min(self.stack, value)
        self.stack -= amount
        self.table.current_pot.add(amount)

    def bet(self, value):
        self.pay(value)
        self.current_bet += min(self.stack, value)
        if self.current_bet > self.table.current_pot.highest_bet:
            self.table.current_pot.highest_bet = self.current_bet
        self.played = True

    def call(self):
        self.bet(self.to_call)

    def post(self, value):
        self.pay(value)
        if value > self.table.current_pot.highest_bet:
            self.table.current_pot.highest_bet = value

    def score_hand(self):
        cards = tuple(card for card in self.combo)
        board = tuple(card for card in self.table.board[:self.table.board.size])
        score = self.table.evaluator.evaluate(cards=cards, board=board)
        return score

    def evaluate_hand(self):
        score = self.score_hand()
        rank_class = self.table.evaluator.get_rank_class(score)
        class_str = self.table.evaluator.rank_to_string(rank_class)
        return {"score": score, "rank": rank_class, "class": class_str}
