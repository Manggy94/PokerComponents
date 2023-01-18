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


class Tournament:
    """Class for played tournaments"""
    _id: str
    _name: str
    _buyin: float
    _is_ko: bool = True
    _money_type: str = "real"
    _level: Level

    def __init__(self, ident: str = '0000', name: str = 'Kill The Fish', is_ko=True, buyin: float = 5.0,
                 money_type: str = 'real', level: Level = Level()):
        self._id = ident
        self._name = name
        self._buyin = buyin
        self.money_type = money_type
        self._is_ko = is_ko
        self._level = level

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
