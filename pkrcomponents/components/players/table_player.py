from attrs import define, field, Factory
from attrs.validators import instance_of, ge, le, optional, max_len, min_len

from pkrcomponents.components.actions.actions_history import ActionsHistory
from pkrcomponents.components.actions.street import Street
from pkrcomponents.components.cards.combo import Combo
from pkrcomponents.components.players.player_hand_stats import PlayerHandStats
from pkrcomponents.components.players.position import Position
from pkrcomponents.components.tables.table import Table
from pkrcomponents.components.utils.converters import convert_to_position
from pkrcomponents.components.utils.exceptions import ShowdownNotReachedError, FullTableError, SeatTakenError


@define(repr=False)
class TablePlayer:
    """
    This class represents a player on a poker table

    Attributes:
        actions_history (ActionsHistory): The history of the player's actions
        bounty (float): The bounty of the player
        combo (Combo): The combo of the player
        current_bet (float): The current bet of the player
        flag_street_first_to_talk (bool): The flag indicating if the player is the first to talk on the street
        flag_street_went_all_in (bool): The flag indicating if the player went all-in on the street
        flag_street_cbet (bool): The flag indicating if the player has made a cbet on the street
        flag_street_donk_bet (bool): The flag indicating if the player has made a donk bet on the street
        folded (bool): Whether the player has folded
        hand_stats (PlayerHandStats): The hand statistics of the player
        has_initiative (bool): Whether the player has initiative
        init_stack (float): The initial stack of the player at the beginning of the hand
        is_hero (bool): Whether the player is the hero
        name (str): The name of the player
        position (Position): The position of the player
        played (bool): Whether the player has played
        hand_reward (int): The reward of the player
        seat (int): The seat number of the player
        stack (float): The current stack of the player
        table (Table): The table the player is on
        went_to_showdown (bool): Whether the player went to showdown

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

    name = field(
        default="Villain",
        validator=[instance_of(str), max_len(12), min_len(3)],
        metadata={'description': 'The name of the player'})
    seat = field(
        default=0,
        validator=[instance_of(int), ge(0), le(10)],
        metadata={'description': 'The seat number of the player'})
    init_stack = field(
        default=0,
        validator=[ge(0), instance_of(float)],
        converter=float,
        metadata={'description': 'The initial stack of the player at the beginning of the hand'})
    stack = field(
        default=Factory(lambda self: self.init_stack, takes_self=True),
        validator=[ge(0), instance_of(float)],
        converter=float,
        metadata={'description': 'The current stack of the player'})
    combo = field(default=None, validator=optional(instance_of(Combo)), converter=Combo)
    folded = field(default=False, validator=instance_of(bool))
    position = field(default=None, validator=optional(instance_of(Position)), converter=convert_to_position)
    table = field(default=None, validator=optional(instance_of(Table)))
    bounty = field(default=0, validator=[ge(0), instance_of(float)], converter=float)
    played = field(default=False, validator=instance_of(bool))
    is_hero = field(default=False, validator=instance_of(bool))
    current_bet = field(default=0, validator=[ge(0), instance_of(float)], converter=float)
    hand_reward = field(default=0, validator=optional([ge(0), instance_of((int, float))]))
    actions_history = field(default=Factory(lambda: ActionsHistory()), validator=instance_of(ActionsHistory))
    hand_stats = field(default=Factory(PlayerHandStats), validator=instance_of(PlayerHandStats))
    has_initiative = field(default=False, validator=instance_of(bool))
    flag_street_first_to_talk = field(default=False, validator=instance_of(bool))
    flag_street_went_all_in = field(default=False, validator=instance_of(bool))
    flag_street_cbet = field(default=False, validator=instance_of(bool))
    flag_street_donk_bet = field(default=False, validator=instance_of(bool))
    went_to_showdown = field(default=False, validator=instance_of(bool))
    entered_hand = field(default=True, validator=instance_of(bool))

    def __repr__(self):
        return (f"TablePlayer(name: '{self.name}', "
                f"seat: {self.seat}, "
                f"stack: {self.stack}, "
                f"position: {self.position}, "
                f"bounty: {self.bounty})")

    def __attrs_post_init__(self):
        self.actions_history.reset()

    @property
    def stack_bb(self) -> float:
        """
        Player's stack in big blinds
        """
        return self.stack / self.table.level.bb

    @property
    def stack_to_pot_ratio(self) -> float:
        """Player's stack to pot ratio"""
        return float("inf") if self.table.pot.value == 0 else self.stack / self.table.pot.value

    @property
    def effective_stack(self) -> float:
        """Player's effective stack"""
        return min(self.stack, max([pl.stack for pl in self.table.players_involved if pl != self]))

    @property
    def stack_enables_raise(self) -> bool:
        """Boolean indicating if the player's stack enables a raise"""
        return self.stack > self.to_call

    @property
    def is_all_in(self) -> bool:
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
    def is_biggest_investor(self) -> bool:
        """Boolean indicating if player is the biggest investor in the pot"""
        return self.invested == max([player.invested for player in self.table.players])

    @property
    def to_call(self) -> float:
        """The amount to call to continue on the table"""
        return self.max_bet(self.table.pot.highest_bet - self.current_bet)

    @property
    def min_raise(self) -> float:
        """The minimum amount to raise"""
        return self.table.min_bet - (self.to_call + self.current_bet)

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
        """Boolean indicating if the player can still play in this street"""
        return not (self.is_all_in or (self.to_call == 0 and self.played) or self.folded)

    @property
    def is_waiting(self):
        """Boolean indicating if the player is waiting his turn to play"""
        return self.can_play and not self.is_ready_for_next_street

    @property
    def is_ready_for_next_street(self):
        """Boolean indicating if the player is ready for the next street"""
        return not self.can_play and self.to_call == 0 and self.played

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
        return (not self.folded) * sum([min(self.invested, player.invested) for player in self.table.players])

    @property
    def has_combo(self) -> bool:
        """Boolean indicating if the player has a known combo"""
        return self.combo is not None

    @property
    def hand_score(self) -> int:
        """Returns player's current hand score on the table"""
        cards = (self.combo.first, self.combo.second)
        board = tuple(card for card in self.table.board.cards[:self.table.board.len])
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
        if table.players.seat_dict.get(self.seat) is not None:
            raise SeatTakenError
        elif table.players.len >= table.max_players:
            raise FullTableError
        else:
            self.table = table
            table.players.add_player(self)
            self.reset_street_status()

    def sit_out(self):
        """Removes player from the table"""
        self.reset_street_status()
        self.table.players.remove_player(self)
        delattr(self, "table")

    def replace(self, table: Table):
        """Replace a player on the table"""
        player_to_replace = table.players.seat_dict.get(self.seat)
        player_to_replace.sit_out()
        self.sit(table)

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
        self.hand_stats.general.combo = combo

    def shows(self, combo: (Combo, str)):
        """
        The player shows a combo at showdown

        Args:
            combo (Combo, str): The combo to show
        """
        if self.table.street != Street.SHOWDOWN and not self.table.hand_ended:
            raise ShowdownNotReachedError()
        self.combo = Combo(combo)
        self.hand_stats.general.combo = self.combo
        self.went_to_showdown = True
        self.hand_stats.general.flag_went_to_showdown = True
        if self.has_table and not self.is_hero:
            self.table.deck.draw(self.combo.first)
            self.table.deck.draw(self.combo.second)

    def delete_combo(self):
        """Deletes a player's combo"""

        if self.has_table and self.has_combo:
            self.table.deck.replace(self.combo.first)
            self.table.deck.replace(self.combo.second)
        self.combo = None


    def update_has_position_stat(self):
        """Update has position stat"""
        if self.is_in_position:
            match self.table.street:
                case Street.FLOP:
                    self.hand_stats.flop.flag_has_position = True
                case Street.TURN:
                    self.hand_stats.turn.flag_has_position = True
                case Street.RIVER:
                    self.hand_stats.river.flag_has_position = True

    def reset_street_status(self):
        """Reset street status"""
        self.played = False
        self.current_bet = 0
        self.flag_street_first_to_talk = False
        self.flag_street_went_all_in = False
        self.flag_street_cbet = False
        self.flag_street_donk_bet = False

    def reset_actions(self):
        """Reset actions"""
        self.actions_history.reset()

    def reset_hand_status(self):
        """Reset hand status"""
        self.reset_street_status()
        self.folded = False
        self.went_to_showdown = False
        self.reset_init_stack()
        self.delete_combo()
        self.reset_actions()

    def pay(self, value: float):
        """
        Action of paying a value

        Args:
            value (float): The amount to pay
        """
        amount = self.max_bet(value)
        self.stack -= amount
        self.table.pot.add(amount)

    def win(self, amount: float) -> None:
        """
        Gives player a certain amount from the pot

        Args:
            amount (float): The amount to win
        """
        self.stack += amount
        self.hand_stats.general.amount_won = amount


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

    def take_initiative(self):
        """Player takes initiative"""
        for player in self.table.players:
            player.has_initiative = False
        self.has_initiative = True

    def set_first_to_talk(self):
        """Sets the first to talk flag to True if player is the first to talk"""
        if not any([player.flag_street_first_to_talk for player in self.table.players_in_game]):
            self.flag_street_first_to_talk = True

    @property
    def is_in_position(self) -> bool:
        """
        Boolean indicating if player is in position
        """
        return self.table.players_in_game[-1] == self

    @property
    def can_1bet(self) -> bool:
        """Boolean indicating if player can 1bet"""
        return self.table.cnt_bets == 0 and self.stack_enables_raise

    @property
    def can_2bet(self) -> bool:
        """Boolean indicating if player can 2bet"""
        return self.table.cnt_bets == 1 and self.stack_enables_raise

    @property
    def can_3bet(self) -> bool:
        """Boolean indicating if player can 3bet"""
        return self.table.cnt_bets == 2 and self.stack_enables_raise

    @property
    def can_4bet(self) -> bool:
        """Boolean indicating if player can 4bet"""
        return self.table.cnt_bets >= 3 and self.stack_enables_raise

    @property
    def can_cbet(self) -> bool:
        """Boolean indicating if player can cbet"""
        return self.has_initiative and self.can_open

    @property
    def can_donk_bet(self) -> bool:
        """Boolean indicating if player can donk bet"""
        return not self.has_initiative and self.can_open and any([player.has_initiative
                                                                  for player in self.table.players_able_to_play])

    @property
    def can_raise(self) -> bool:
        """Boolean indicating if player can raise"""
        return self.table.cnt_bets >= 1 and self.stack_enables_raise

    @property
    def can_first_raise(self) -> bool:
        """Boolean indicating if player can make the first raise"""
        return self.is_facing_1bet and self.stack_enables_raise

    @property
    def can_open(self) -> bool:
        """Boolean indicating if player can open"""
        return ((self.table.street.is_preflop and not self.table.is_opened)
                or (not self.table.street.is_preflop and self.table.cnt_bets == 0))

    @property
    def can_squeeze(self) -> bool:
        """Boolean indicating if player can squeeze"""
        return self.can_3bet and self.table.cnt_cold_calls > 0 and self.table.street.is_preflop

    @property
    def can_steal(self) -> bool:
        """Boolean indicating if player can steal"""
        return self.can_open and self.position.is_steal and self.table.street.is_preflop

    @property
    def is_facing_raise(self) -> bool:
        """Boolean indicating if player faces a raise"""
        return self.table.cnt_bets >= 2

    @property
    def is_facing_1bet(self) -> bool:
        """Boolean indicating if player is facing a 1bet"""
        return self.table.cnt_bets == 1

    @property
    def is_facing_2bet(self) -> bool:
        """Boolean indicating if player is facing a 2bet"""
        return self.table.cnt_bets == 2

    @property
    def is_facing_3bet(self) -> bool:
        """Boolean indicating if player is facing a 3bet"""
        return self.table.cnt_bets == 3

    @property
    def is_facing_4bet(self) -> bool:
        """Boolean indicating if player is facing a 4bet"""
        return self.table.cnt_bets >= 4

    @property
    def is_facing_squeeze(self) -> bool:
        """Boolean indicating if player is facing a squeeze"""
        return (self.is_facing_3bet
                and any([player.hand_stats.preflop.flag_squeeze for player in self.table.players_involved])
                and self.table.street.is_preflop)

    @property
    def is_facing_steal(self) -> bool:
        """Boolean indicating if player is facing a steal"""
        return (
                self.is_facing_2bet
                and any([player.hand_stats.preflop.flag_steal_attempt for player in self.table.players_involved])
                and self.table.street.is_preflop)

    @property
    def is_defending_blinds(self) -> bool:
        """Boolean indicating if player is defending blinds"""
        return self.is_facing_raise and self.position.is_blind and self.table.street.is_preflop

    @property
    def is_facing_cbet(self) -> bool:
        """Boolean indicating if player is facing a cbet"""
        return self.is_facing_1bet and any([player.flag_street_cbet for player in self.table.players_involved])

    @property
    def is_facing_donk_bet(self) -> bool:
        """Boolean indicating if player is facing a donk bet"""
        return self.is_facing_1bet and any([player.flag_street_donk_bet for player in self.table.players_involved])

    @property
    def is_facing_covering_bet(self) -> bool:
        """Boolean indicating if player is facing a covering bet"""
        return self.to_call >= self.stack

    @property
    def is_facing_all_in(self) -> bool:
        """Boolean indicating if player is facing an all-in"""
        return any([player.flag_street_went_all_in for player in self.table.players_involved])
