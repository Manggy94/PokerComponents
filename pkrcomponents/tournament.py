from pkrcomponents.constants import MoneyType


class Buyin:
    """
    A class for the buy-in of a tournament
    """
    _freeze_part: float
    _ko_part: float
    _rake: float

    def __init__(self, freeze: float, ko: float, rake: float):
        self._freeze_part = freeze
        self._ko_part = ko
        self._rake = rake

    @property
    def freeze_part(self):
        return self._freeze_part

    @freeze_part.setter
    def freeze_part(self, freeze):
        if freeze < 0:
            raise ValueError("Freeze part must be positive")
        self._freeze_part = freeze

    @property
    def ko_part(self):
        return self._ko_part

    @ko_part.setter
    def ko_part(self, ko):
        if ko < 0:
            raise ValueError("KO part must be positive")
        self._ko_part = ko

    @property
    def rake(self):
        return self._rake

    @rake.setter
    def rake(self, rake):
        if rake < 0:
            raise ValueError("Rake must be positive")
        self._rake = rake

    @property
    def total(self):
        return self.freeze_part + self.ko_part + self.rake

    @classmethod
    def from_total(cls, total: float):
        freeze = total * 0.45
        ko = total * 0.45
        rake = total * 0.1
        return cls(freeze, ko, rake)

    def __str__(self):
        return f"Buy-in: {self.total}"

    def __eq__(self, other):
        return self.freeze_part == other.freeze_part and self.ko_part == other.ko_part and self.rake == other.rake

    def to_json(self):
        return {
            "freeze": self.freeze_part,
            "ko": self.ko_part,
            "rake": self.rake
        }


class Level:
    """Level of the tournament"""

    _value: int
    _sb: float
    _bb: float
    _ante: float

    def __init__(self, value: int = 1,  bb: float = 200.0, ante=None):
        self._value = value
        self.bb = float(bb)
        if ante is None:
            self._ante = bb*0.125
        else:
            self._ante = ante

    def __str__(self):
        return f"Current level: {self.value}\nAnte={self.ante}\nSB={self.sb}\nBB={self.bb}"

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
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value):
        if value < 0 or not isinstance(value, int):
            raise ValueError("Level must be a positive int")
        else:
            self._value = value

    def to_json(self):
        return {
            "value": self.value,
            "ante": self.ante,
            "sb": self.sb,
            "bb": self.bb
        }


class Payout:
    """
    A class for a payout in a tournament
    """
    _tier: int
    _reward: float

    def __init__(self, tier: int, reward: float):
        self._tier = tier
        self._reward = reward

    def __str__(self):
        return f"Tier: {self.tier} - Reward: {self.reward}"

    @property
    def tier(self) -> int:
        return self._tier

    @tier.setter
    def tier(self, tier):
        if tier < 0 or not isinstance(tier, int):
            raise ValueError("Tier must be a positive integer")
        self._tier = tier

    @property
    def reward(self) -> float:
        return self._reward

    @reward.setter
    def reward(self, reward):
        if reward < 0 or not isinstance(reward, float):
            raise ValueError("Reward must be positive")
        self._reward = reward


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

    def get_prize_pool(self) -> float:
        """
        A method to get the total prize pool distributed via the payouts
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
    _buyin: Buyin
    _is_ko: bool = True
    _money_type: str = "real"
    _level: Level
    _payouts: Payouts
    _players_remaining: int
    _total_players: int
    _starting_stack: float

    def __init__(self,
                 ident: str = '0000',
                 name: str = 'Kill The Fish',
                 is_ko=True,
                 buyin: Buyin = Buyin(2.25, 2.25, 0.5),
                 money_type: str = 'real',
                 level: Level = Level(),
                 starting_stack: float = 20000,
                 total_players: int = None,
                 players_remaining: int = None
                 ):
        self._id = ident
        self._name = name
        self._buyin = buyin
        self.money_type = money_type
        self._is_ko = is_ko
        self._level = level
        self._starting_stack = starting_stack
        self._total_players = total_players
        self._players_remaining = players_remaining

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
    def buyin(self, buyin: Buyin):
        self._buyin = buyin

    @property
    def money_type(self):
        return self._money_type

    @money_type.setter
    def money_type(self, money_type):
        self._money_type = MoneyType(money_type)

    @property
    def level(self) -> Level:
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

    @payouts.setter
    def payouts(self, payouts):
        self._payouts = payouts

    @property
    def total_players(self):
        return self._total_players

    @total_players.setter
    def total_players(self, total_players):
        if total_players < 0 or not isinstance(total_players, int):
            raise ValueError("Total players must be a positive integer")
        self._total_players = total_players

    @property
    def players_remaining(self) -> int:
        return self._players_remaining

    @players_remaining.setter
    def players_remaining(self, players_remaining):
        if players_remaining < 0 or players_remaining > self.total_players:
            raise ValueError("Players remaining must be a positive integer and less than total players")
        self._players_remaining = players_remaining

    @property
    def starting_stack(self):
        return self._starting_stack

    @starting_stack.setter
    def starting_stack(self, starting_stack):
        if starting_stack < 0:
            raise ValueError("Starting stack must be positive")
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

    def __str__(self):
        return f"Name: {self.name}\nId: {self.id}\nBuy-in: {self.buyin}\nMoney: {self.money_type}"

    def to_json(self):
        return {
            "level": self.level.to_json(),
            "id": self.id,
            "name": self.name,
            "buy_in": self.buyin.to_json(),
            "is_ko": self.is_ko,
            "money_type": self.money_type
        }
