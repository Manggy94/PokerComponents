from pkrcomponents.constants import Position, Street
from pkrcomponents.hand import Combo
from pkrcomponents.table import Table


class TablePlayer:
    """
    Class Representing a player that sits to play poker on a table
    """

    _name: str
    _seat: int
    _stack: float
    _init_stack: float
    _combo: Combo or None
    _folded: bool
    _hero: bool
    _position: Position or None
    _table: Table
    _max_reward: float

    def __init__(self, name: str = "Villain", seat=0, stack: float = 0):
        self.name = name
        self.seat = seat
        if stack < 0:
            raise ValueError("Init stack cannot be negative")
        else:
            self.stack = stack
            self.init_stack = stack
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
        """Player's name"""
        return self._name

    @name.setter
    def name(self, name: str):
        """Setter for player's name"""
        if len(name) > 12:
            raise ValueError("Player name length should be between 3 and 12 characters")
        else:
            self._name = name

    @property
    def seat(self):
        """Player's seat"""
        return self._seat

    @seat.setter
    def seat(self, seat):
        """Setter for player's seat"""
        if seat not in range(11):
            raise ValueError("Seat should be an int between 0 and 10")
        else:
            self._seat = seat

    @property
    def stack(self):
        """Player's stack"""
        return self._stack

    @stack.setter
    def stack(self, stack):
        """Setter for player's stack"""
        self._stack = max(0.0, float(stack))

    @property
    def folded(self):
        """Boolean indicating if player folded"""
        return self._folded

    @folded.setter
    def folded(self, folded):
        """Setter for Boolean indicating if player folded"""
        self._folded = folded

    @property
    def init_stack(self):
        """Returns player's stack at the beginning of the hand"""
        return self._init_stack

    @init_stack.setter
    def init_stack(self, stack):
        """Setter for player's stack at the beginning of the hand"""
        self._init_stack = max(0.0, float(stack))
        self.stack = self.init_stack

    @property
    def table(self):
        """Returns associated table"""
        return self._table

    @property
    def has_table(self):
        """Boolean indicating if player has a table"""
        return hasattr(self, "table")

    @property
    def invested(self):
        """Float indicating the amount already invested by a player in pot"""
        return self.init_stack - self.stack

    @property
    def max_reward(self):
        """Float indicating the maximum amount that can be won by the player"""
        return (not self.folded) * sum([min(self.invested, pl.invested) for pl in self.table.players])

    @property
    def combo(self):
        """PLayer's Combo"""
        return self._combo

    @combo.setter
    def combo(self, combo: Combo):
        """Setter for Player's combo"""
        combo = Combo(combo)
        self._combo = combo

    @property
    def has_combo(self) -> bool:
        """Boolean indicating if the player has a known combo"""
        return self._combo is not None

    @property
    def is_hero(self) -> bool:
        """Returns if the player is the hero"""
        return self._hero

    @is_hero.setter
    def is_hero(self, is_hero):
        """Setter to (un)make the player a hero"""
        self._hero = is_hero

    def shows(self, combo):
        """The player shows a combo at showdown"""
        self.combo = combo
        if self.has_table:
            self.table.deck.draw(self.combo.first)
            self.table.deck.draw(self.combo.second)

    @property
    def position(self):
        """Returns player's position (ex: UTG, BTN, BB)"""
        return self._position

    @position.setter
    def position(self, position):
        """Setter for player's position"""
        position = Position(position)
        self._position = position

    def distribute(self, combo):
        """Distributes a combo to a player"""
        combo = Combo(combo)
        self.table.deck.draw(combo.first)
        self.table.deck.draw(combo.second)
        self.combo = combo

    def reset_street_status(self):
        """Reset street status"""
        self.played = False
        self.current_bet = 0

    @property
    def to_call(self):
        """float indicating the amount to call to continue on the table"""
        return min(self.table.pot.highest_bet-self.current_bet, self.stack)

    @property
    def is_all_in(self):
        """Boolean indicating if the player is all-in"""
        return self.stack == 0

    @property
    def can_play(self):
        """Boolean indicating if the player can still play in this hand"""
        return not (self.is_all_in or (self.to_call == 0 and self.played) or self.folded)

    @property
    def in_game(self):
        """Boolean indicating if the player can still make actions in this hand"""
        return not (self.is_all_in or self.folded)

    @property
    def pot_odds(self) -> float:
        """Float indicating pot odds"""
        to_call = self.to_call
        if to_call != 0:
            pot_odds = float(self.table.pot.value/to_call)
        else:
            pot_odds = float("inf")
        return pot_odds

    @property
    def req_equity(self):
        """Float indicating minimum required equity for an EV+ call"""
        return 1.0/(1.0+self.pot_odds)

    def max_bet(self, value):
        """Returns the real amount in a bet"""
        return min(self.stack, value)

    def sit(self, table):
        """Sits a player on a table"""
        if table.players.len < table.max_players and table.players.seat_dict.get(self.seat) is None:
            self._table = table
            self.table.players.pl_list.append(self)
            self.table.players.name_dict[self.name] = self
            self.table.players.seat_dict[self.seat] = self
            self.reset_street_status()

    def sit_out(self):
        """Removes player from the table"""
        self.reset_street_status()
        self.table.players.pl_list.remove(self)
        self.table.players.name_dict.pop(self.name)
        self.table.players.seat_dict.pop(self.seat)
        delattr(self, "_table")

    def pay(self, value):
        """Action of paying a value"""
        amount = self.max_bet(value)
        self.stack -= amount
        self.table.pot.add(amount)

    def do_bet(self, value):
        """Action of betting a certain value"""
        self.current_bet += self.max_bet(value)
        self.pay(value)
        if self.current_bet > self.table.pot.highest_bet:
            self.table.pot.highest_bet = self.current_bet
        self.played = True

    def bet(self, value):
        """Bet and step to next player"""
        if value >= self.table.min_bet:
            self.table.min_bet = 2*value - self.table.pot.highest_bet
            self.do_bet(value)
        elif self.table.min_bet > self.stack:
            self.bet(self.table.min_bet)
        else:
            raise ValueError(f"You cannot bet {value} if the minimum bet is {self.table.min_bet} "
                             f"and your stack is {self.stack}")
        self.table.advance_seat_playing()

    def do_call(self):
        """Action of calling"""
        self.do_bet(self.to_call)

    def call(self):
        """Call and step to next player"""
        self.do_call()
        self.table.advance_seat_playing()

    def do_check(self):
        """Action of checking"""
        if self.to_call != 0:
            raise ValueError("A player cannot check if somebody bet before")
        else:
            self.played = True

    def check(self):
        """Check and step to next player"""
        self.do_check()
        self.table.advance_seat_playing()

    def do_fold(self):
        """Action of folding"""
        self.folded = True
        self.played = True

    def fold(self):
        """Fold and step to next player"""
        self.do_fold()
        self.table.advance_seat_playing()

    def post(self, value):
        """Action of posting"""
        self.pay(value)
        if value > self.table.pot.highest_bet:
            self.table.pot.highest_bet = value

    @property
    def hand_score(self):
        """Returns player's current hand score on the table"""
        cards = (self.combo.first, self.combo.second)
        board = tuple(card for card in self.table.board[:self.table.board.len])
        score = self.table.evaluator.evaluate(cards=cards, board=board)
        return score

    @property
    def rank_class(self):
        """Returns player's current hand rank class on the table"""
        return self.table.evaluator.get_rank_class(self.hand_score)

    @property
    def class_str(self):
        """Returns player's current hand rank class on the table"""
        return self.table.evaluator.score_to_string(self.hand_score)

    def win(self, amount):
        """gives player a certain amount from the pot"""
        self.table.pot.value -= amount
        self.stack += amount
