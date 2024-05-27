from attrs import define, field, Factory
from attrs.validators import instance_of, ge, le, optional, max_len, min_len

from pkrcomponents.constants import Position, Street
from pkrcomponents.hand import Combo
from pkrcomponents.table import Table
from pkrcomponents.utils.converters import convert_to_position


@define
class TablePlayer:
    """Class Representing a player that sits to play poker on a table"""

    name = field(default="Villain", validator=[instance_of(str), max_len(12), min_len(3)])
    seat = field(default=0, validator=[instance_of(int), ge(0), le(10)])
    init_stack = field(default=0, validator=[ge(0), instance_of(float)], converter=float)
    stack = field(default=Factory(lambda self: self.init_stack, takes_self=True),
                  validator=[ge(0), instance_of(float)], converter=float)

    combo = field(default=None, validator=optional(instance_of(Combo)), converter=Combo)
    folded = field(default=False, validator=instance_of(bool))
    hero = field(default=False, validator=instance_of(bool))
    position = field(default=None, validator=optional(instance_of(Position)), converter=convert_to_position)
    table = field(default=None, validator=optional(instance_of(Table)))
    bounty = field(default=0, validator=[ge(0), instance_of(float)], converter=float)
    played = field(default=False, validator=instance_of(bool))
    is_hero = field(default=False, validator=instance_of(bool))
    current_bet = field(default=0, validator=[ge(0), instance_of(float)], converter=float)
    reward = field(default=0, validator=optional([ge(0), instance_of((int, float))]))
    actions = field(default={
        f"{Street('Preflop')}": [],
        f"{Street('Flop')}": [],
        f"{Street('Turn')}": [],
        f"{Street('River')}": []
    }, validator=instance_of(dict))

    @property
    def stack_bb(self):
        """Player's stack in big blinds"""
        return self.stack / self.table.level.bb

    @property
    def stack_to_pot_ratio(self):
        """Player's stack to pot ratio"""
        return float("inf") if self.table.pot.value == 0 else self.stack / self.table.pot.value

    @property
    def is_all_in(self):
        """Boolean indicating if the player is all-in"""
        return self.stack == 0

    @property
    def m_factor(self) -> float:
        """Player's M factor"""
        return round(self.stack / self.table.cost_per_round, 2)

    @property
    def m_factor_eff(self) -> float:
        """Player's effective M factor"""
        return round(self.m_factor * (self.table.players.len / 10), 2)

    @property
    def has_table(self):
        """Boolean indicating if player has a table"""
        return hasattr(self, "table")

    @property
    def invested(self):
        """Float indicating the amount already invested by a player in pot"""
        return self.init_stack - self.stack

    @property
    def to_call(self):
        """float indicating the amount to call to continue on the table"""
        return min(self.table.pot.highest_bet - self.current_bet, self.stack)

    @property
    def to_call_bb(self):
        """float indicating the amount to call to continue on the table in big blinds"""
        return self.to_call / self.table.level.bb

    @property
    def is_current_player(self):
        """Boolean indicating if the player is the current player"""
        if not self.can_play and self.table.current_player == self:
            self.table.advance_seat_playing()
            return False
        return self.table.current_player == self

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
        return float("inf") if self.to_call == 0 else float(self.table.pot.value / self.to_call)

    @property
    def req_equity(self):
        """Float indicating minimum required equity for an EV+ call"""
        return 1.0 / (1.0 + self.pot_odds)

    def max_bet(self, value):
        """Returns the real amount in a bet"""
        return min(self.stack, value)

    @property
    def max_reward(self):
        """Float indicating the maximum amount that can be won by the player"""
        return (not self.folded) * sum([min(self.invested, pl.invested) for pl in self.table.players])

    @property
    def has_combo(self) -> bool:
        """Boolean indicating if the player has a known combo"""
        return self.combo is not None

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

    def sit(self, table):
        """Sits a player on a table"""
        if table.players.len < table.max_players and table.players.seat_dict.get(self.seat) is None:
            self.table = table
            table.players.add_player(self)
            self.reset_street_status()

    def sit_out(self):
        """Removes player from the table"""
        self.reset_street_status()
        self.table.players.remove_player(self)
        delattr(self, "table")

    def reset_init_stack(self):
        """Reset player's initial stack"""
        if self.stack == 0:
            self.table.remove_player(self)
        self.init_stack = self.stack

    def distribute(self, combo):
        """Distributes a combo to a player"""
        combo = Combo(combo)
        self.table.deck.draw(combo.first)
        self.table.deck.draw(combo.second)
        self.combo = combo

    def shows(self, combo: (Combo, str)):
        """The player shows a combo at showdown"""
        self.combo = Combo(combo)
        if self.has_table:
            self.table.deck.draw(self.combo.first)
            self.table.deck.draw(self.combo.second)

    def delete_combo(self):
        """Deletes a player's combo"""
        if self.has_combo:
            self.table.deck.replace(self.combo.first)
            self.table.deck.replace(self.combo.second)
            self.combo = None

    def reset_street_status(self):
        """Reset street status"""
        self.played = False
        self.current_bet = 0

    def reset_hand_status(self):
        """Reset hand status"""
        self.reset_street_status()
        self.folded = False
        self.reset_init_stack()
        self.delete_combo()

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
            self.table.cnt_bets += 1
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

    def win(self, amount):
        """gives player a certain amount from the pot"""
        self.table.pot.value -= amount
        self.stack += amount

    @property
    def preflop_bet_amounts(self):
        bet_amounts = [round(self.table.min_bet * factor) for factor in self.table.preflop_bet_factors]
        bet_amounts = [amt for amt in bet_amounts if amt < self.stack]
        bet_amounts.append(self.stack)
        return bet_amounts

    @property
    def postflop_bets(self):
        postflop_bets = [
            {"text": factor.get("text"), "value": round(self.table.pot.value * factor.get("value"))}
            for factor in self.table.postflop_bet_factors
        ]
        postflop_bets = [bet for bet in postflop_bets
                         if self.table.min_bet < bet.get("value") < self.stack]
        postflop_bets.append({"text": "All-in", "value": self.stack})
        if self.table.min_bet < self.stack:
            postflop_bets.append({"text": "Min Bet", "value": self.table.min_bet})
        postflop_bets = sorted(postflop_bets, key=lambda x: x.get("value"))
        return postflop_bets
