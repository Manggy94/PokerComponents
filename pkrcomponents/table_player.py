from attrs import define, field, Factory
from attrs.validators import instance_of, ge, le, optional, max_len, min_len

from pkrcomponents.constants import Position, Street
from pkrcomponents.hand import Combo
from pkrcomponents.table import Table
from pkrcomponents.utils.converters import convert_to_position


@define
class TablePlayer:
    """
    This class represents a player on a poker table

    Attributes:
        name(str): The name of the player
        seat(int): The seat number of the player
        init_stack(float): The initial stack of the player at the beginning of the hand
        stack(float): The current stack of the player
        combo(Combo): The combo of the player
        folded(bool): Whether the player has folded
        position(Position): The position of the player
        table(Table): The table the player is on
        bounty(float): The bounty of the player
        played(bool): Whether the player has played
        is_hero(bool): Whether the player is the hero
        current_bet(float): The current bet of the player
        reward(int): The reward of the player
        actions(dict): The actions of the player on each street

    Methods:
        stack_bb(): Returns the player's stack in big blinds
        stack_to_pot_ratio(): Returns the player's stack to pot ratio
        is_all_in(): Returns whether the player is all-in
        m_factor(): Returns the player's M factor
        m_factor_eff(): Returns the player's effective M factor
        has_table(): Returns whether the player has a table
        invested(): Returns the amount already invested by the player in the pot
        to_call(): Returns the amount to call to continue on the table
        to_call_bb(): Returns the amount to call to continue on the table in big blinds
        is_current_player(): Returns whether the player is the current player
        can_play(): Returns whether the player can still play in this hand
        in_game(): Returns whether the player can still make actions in this hand
        pot_odds(): Returns the pot odds
        req_equity(): Returns the minimum required equity for an EV+ call
        max_bet(value): Returns the real amount in a bet
        max_reward(): Returns the maximum amount that can be won by the player
        has_combo(): Returns whether the player has a known combo
        hand_score(): Returns the player's current hand score on the table
        rank_class(): Returns the player's current hand rank class on the table
        class_str(): Returns the player's current hand rank class on the table
        sit(table): Sits the player on a table
        sit_out(): Removes the player from the table
        reset_init_stack(): Resets the player's initial stack
        distribute(combo): Distributes a combo to the player
        shows(combo): The player shows a combo at showdown
        delete_combo(): Deletes the player's combo
        reset_street_status(): Resets street status
        reset_hand_status(): Resets hand status
        pay(value): Action of paying a value
        do_bet(value): Action of betting a certain value
        bet(value): Bet and step to next player
        do_call(): Action of calling
        call(): Call and step to next player
        do_check(): Action of checking
        check(): Check and step to next player
        do_fold(): Action of folding
        fold(): Fold and step to next player
        post(value): Action of posting
        win(amount): Gives the player a certain amount from the pot
        preflop_bet_amounts(): Returns preflop bet amounts
        postflop_bets(): Returns postflop bets

    """

    name = field(default="Villain", validator=[instance_of(str), max_len(12), min_len(3)])
    seat = field(default=0, validator=[instance_of(int), ge(0), le(10)])
    init_stack = field(default=0, validator=[ge(0), instance_of(float)], converter=float)
    stack = field(default=Factory(lambda self: self.init_stack, takes_self=True),
                  validator=[ge(0), instance_of(float)], converter=float)
    combo = field(default=None, validator=optional(instance_of(Combo)), converter=Combo)
    folded = field(default=False, validator=instance_of(bool))
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

    def __repr__(self):
        return (f"\n Name: {self.name}\n "
                f"Seat: {self.seat}\n "
                f"Stack: {self.stack}\n "
                f"Position: {self.position}\n Table: {self.table}\n "
                f"Bounty: {self.bounty}\n")

    @property
    def stack_bb(self) -> float:
        """
        Player's stack in big blinds
        """
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
    def has_table(self) -> bool:
        """Boolean indicating if player has a table"""
        return hasattr(self, "table")

    @property
    def invested(self) -> float:
        """The total amount already invested by a player in pot"""
        return self.init_stack - self.stack

    @property
    def to_call(self) -> float:
        """The amount to call to continue on the table"""
        return self.max_bet(self.table.pot.highest_bet - self.current_bet)

    @property
    def to_call_bb(self):
        """The amount to call to continue on the table in big blinds"""
        return self.to_call / self.table.level.bb

    @property
    def is_current_player(self) -> bool:
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

    def max_bet(self, value: float) -> float:
        """
        Returns the real amount in a bet

        Args:
            value (float): The amount to bet
        """
        return min(self.stack, value)

    @property
    def max_reward(self) -> float:
        """Float indicating the maximum amount that can be won by the player"""
        return (not self.folded) * sum([min(self.invested, pl.invested) for pl in self.table.players])

    @property
    def has_combo(self) -> bool:
        """Boolean indicating if the player has a known combo"""
        return self.combo is not None

    @property
    def hand_score(self) -> int:
        """Returns player's current hand score on the table"""
        cards = (self.combo.first, self.combo.second)
        board = tuple(card for card in self.table.board[:self.table.board.len])
        score = self.table.evaluator.evaluate(cards=cards, board=board)
        return score

    @property
    def rank_class(self) -> int:
        """Returns player's current hand rank class on the table"""
        return self.table.evaluator.get_rank_class(self.hand_score)

    @property
    def class_str(self) -> str:
        """Returns player's current hand rank class on the table"""
        return self.table.evaluator.score_to_string(self.hand_score)

    def sit(self, table: Table):
        """
        Sits a player on a table

        Args:
            table (Table): The table to sit the player on
        """
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

    def distribute(self, combo: (Combo, str)):
        """
        Distributes a combo to a player

        Args:
            combo (Combo, str): The combo to distribute
        """
        combo = Combo(combo)
        self.table.deck.draw(combo.first)
        self.table.deck.draw(combo.second)
        self.combo = combo

    def shows(self, combo: (Combo, str)):
        """
        The player shows a combo at showdown

        Args:
            combo (Combo, str): The combo to show
        """
        if self.table.street != Street.SHOWDOWN:
            raise ValueError("Player cannot show combo if it is not showdown")
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

    def pay(self, value: float):
        """
        Action of paying a value

        Args:
            value (float): The amount to pay
        """
        amount = self.max_bet(value)
        self.stack -= amount
        self.table.pot.add(amount)

    def do_bet(self, value: float):
        """
        Action of betting a certain value

        Args:
            value (float): The amount to bet
        """
        self.current_bet += self.max_bet(value)
        self.pay(value)
        if self.current_bet > self.table.pot.highest_bet:
            self.table.pot.highest_bet = self.current_bet
            self.table.cnt_bets += 1
        self.played = True

    def post(self, value: float):
        """
        Action of posting

        Args:
            value (float): The amount to post
        """
        self.pay(value)
        if value > self.table.pot.highest_bet:
            self.table.pot.highest_bet = value

    def win(self, amount: float) -> None:
        """
        Gives player a certain amount from the pot

        Args:
            amount (float): The amount to win
        """
        self.table.pot.value -= amount
        self.stack += amount

    @property
    def preflop_bet_amounts(self) -> list:
        """Returns preflop bet amounts for the player"""
        bet_amounts = [round(self.table.min_bet * factor)
                       for factor in self.table.preflop_bet_factors
                       if round(self.table.min_bet * factor) < self.stack]
        bet_amounts.append(self.stack)
        return bet_amounts

    @property
    def postflop_bets(self) -> list:
        """
        Returns postflop bets for the player
        """
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
