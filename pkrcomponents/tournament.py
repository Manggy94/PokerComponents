from attrs import define, field, asdict, Factory
from attrs.validators import instance_of,  ge, gt, le

from pkrcomponents.constants import MoneyType
from pkrcomponents.level import Level
from pkrcomponents.payout import Payouts
from pkrcomponents.buy_in import BuyIn
from pkrcomponents.utils.validators import validate_players_remaining


@define
class Tournament:
    """Class for played tournaments"""
    id = field(default='0000', validator=[instance_of(str)])
    name = field(default='Kill The Fish', validator=[instance_of(str)])
    buyin = field(default=Factory(BuyIn), validator=[instance_of(BuyIn)])
    is_ko = field(default=True, validator=[instance_of(bool)])
    money_type = field(default=MoneyType.REAL, validator=[instance_of(MoneyType)])
    level = field(default=Factory(Level), validator=[instance_of(Level)])
    payouts = field(default=Factory(Payouts), validator=[instance_of(Payouts)])
    total_players = field(default=2, validator=[gt(1), instance_of(int)])
    players_remaining = field(default=2, validator=validate_players_remaining)
    starting_stack = field(default=20000.0, validator=[gt(0), instance_of((float, int))])

    def __str__(self):
        return f"Name: {self.name}\nId: {self.id}\nBuy-in: {self.buyin}\nMoney: {self.money_type}"

    @property
    def total_chips(self):
        return self.total_players * self.starting_stack

    @property
    def average_stack(self):
        return self.total_chips / self.players_remaining

    @property
    def players_eliminated(self):
        return self.total_players - self.players_remaining

    @property
    def tournament_progression(self):
        return self.players_eliminated / (self.total_players - 1)

    @property
    def next_tier(self):
        return self.payouts.closest_payout(self.players_remaining).tier

    @property
    def next_reward(self):
        return self.payouts.closest_payout(self.players_remaining).reward

    @property
    def players_to_next_tier(self):
        return self.players_remaining - self.payouts.closest_payout(self.players_remaining).tier

    def estimated_players_remaining(self, average_stack: float) -> int:
        """
        Estimate the number of players remaining in the tournament based on the average stack of the remaining players
        """
        return min(round(self.total_chips / average_stack), self.total_players)

    def to_json(self):
        return {
            "level": self.level.to_json(),
            "id": self.id,
            "name": self.name,
            "buy_in": self.buyin.to_json(),
            "is_ko": self.is_ko,
            "money_type": self.money_type
        }
