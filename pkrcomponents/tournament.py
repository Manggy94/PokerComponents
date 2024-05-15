from pkrcomponents.constants import MoneyType


class Level:
    """Level of the tournament"""

    _level: int
    _sb: float
    _bb: float
    _ante: float

    def __init__(self, level: int = 1,  bb: float = 200.0, ante=None):
        self._level = level
        self.bb = float(bb)
        if ante is None:
            self._ante = bb*0.125
        else:
            self._ante = ante

    def __str__(self):
        return f"Current level: {self.level}\nAnte={self.ante}\nSB={self.sb}\nBB={self.bb}"

    @property
    def bb(self) -> float:
        """"""
        return self._bb

    @bb.setter
    def bb(self, bb):
        if bb < 0:
            raise ValueError("BB Value must be positive")
        else:
            self._bb = bb
            self._sb = bb/2

    @property
    def sb(self):
        return self._sb

    @property
    def ante(self):
        return self._ante

    @ante.setter
    def ante(self, ante):
        if ante < 0:
            raise ValueError("Ante must be positive")
        else:
            self._ante = ante

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        if level < 0 or type(level) != int:
            raise ValueError("Level must be a positive int")
        else:
            self._level = level

    def to_json(self):
        return {
            "level": self.level,
            "ante": self.ante,
            "sb": self.sb,
            "bb": self.bb
        }


class Payout:
    """
    A class for a payout in a tournament
    """
    def __init__(self, tier: int, reward: float):
        self.tier = tier
        self.reward = reward

    def __str__(self):
        return f"Tier: {self.tier} - Reward: {self.reward}"


class Payouts(list):
    """
    A list of payouts
    """

    def add_payout(self, payout: Payout):
        """
        A method to add a payout to the list
        """
        self.append(payout)

    def remove_payout(self, tier: int):
        """
        A method to remove a payout from the list
        """
        for payout in self:
            if payout.tier == tier:
                self.remove(payout)
                return True
        return False

    def get_payout(self, rank: int) -> Payout:
        """
        A method to get the reward for a given finish rank
        """
        for tier, reward in zip(self.tiers, self.rewards):
            if tier >= rank:
                return Payout(tier, reward)
        return Payout(0, 0.0)

    def closest_payout(self, rank: int) -> Payout:
        """
        A method to get the closest payout to a given rank
        """
        i = 0
        while i < len(self) and rank > self[i].tier:
            i += 1
        return self[i-1]

    def get_reward(self, rank: int) -> float:
        """
        A method to get the reward for a given finish rank
        """
        return self.get_payout(rank).reward

    def get_prizepool(self) -> float:
        """
        A method to get the total prizepool distributed via the payouts
        """
        return sum(self.get_reward(rank) for rank in range(1, max(self.tiers)+1))

    @property
    def tiers(self):
        """
        A property to get the tiers of the payouts
        """
        return [payout.tier for payout in self]

    @property
    def rewards(self):
        """
        A property to get the rewards of the payouts
        """
        return [payout.reward for payout in self]


class Tournament:
    """Class for played tournaments"""
    _id: str
    _name: str
    _buyin: float
    _is_ko: bool = True
    _money_type: str = "real"
    _level: Level
    _payouts: Payouts
    _players_remaining: int
    _total_players: int
    _starting_stack: float

    def __init__(self, ident: str = '0000', name: str = 'Kill The Fish', is_ko=True, buyin: float = 5.0,
                 money_type: str = 'real', level: Level = Level(), starting_stack: float = 20000
                 ):
        self._id = ident
        self._name = name
        self._buyin = buyin
        self.money_type = money_type
        self._is_ko = is_ko
        self._level = level
        self._starting_stack = starting_stack

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id_txt: str):
        self._id = id_txt

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name_txt):
        self._name = name_txt

    @property
    def buyin(self):
        return self._buyin

    @buyin.setter
    def buyin(self, amount):
        self._buyin = max(0.0, float(amount))

    @property
    def money_type(self):
        return self._money_type

    @money_type.setter
    def money_type(self, money_type):
        self._money_type = MoneyType(money_type)

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        self._level = level

    @property
    def is_ko(self):
        return self._is_ko

    @is_ko.setter
    def is_ko(self, is_ko):
        self._is_ko = bool(is_ko)

    @property
    def payouts(self):
        return self._payouts

    @property
    def total_players(self):
        return self._total_players

    @total_players.setter
    def total_players(self, total_players):
        self._total_players = total_players

    @property
    def players_remaining(self):
        return self._players_remaining

    @players_remaining.setter
    def players_remaining(self, players_remaining):
        self._players_remaining = players_remaining

    @property
    def starting_stack(self):
        return self._starting_stack

    @starting_stack.setter
    def starting_stack(self, starting_stack):
        self._starting_stack = starting_stack

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
        return self.players_eliminated / self.total_players - 1

    @property
    def next_tier(self):
        return self.payouts.closest_payout(self.players_remaining).tier

    @property
    def next_reward(self):
        return self.payouts.closest_payout(self.players_remaining).reward

    @property
    def players_to_next_tier(self):
        return self.players_remaining - self.payouts.closest_payout(self.players_remaining).tier

    def __str__(self):
        return f"Name: {self.name}\nId: {self.id}\nBuy-in: {self.buyin}\nMoney: {self.money_type}"

    def to_json(self):
        return {
            "level": self.level.to_json(),
            "id": self.id,
            "name": self.name,
            "buy_in": self.buyin,
            "is_ko": self.is_ko,
            "money_type": self.money_type
        }




if __name__ == "__main__":
    p1 = Payout(1, 100.0)
    p2 = Payout(2, 50.0)
    p3 = Payout(3, 25.0)
    p4 = Payout(6, 10.0)
    p5 = Payout(12, 5.0)

    payouts = Payouts([p1, p2, p3, p4, p5])


    print(payouts.get_payout(15), payouts.get_reward(5))
    print(payouts.get_prizepool())
    print(payouts.closest_payout(7))
