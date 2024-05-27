import attrs
from attrs import define, field, Factory, asdict
from attrs.validators import instance_of, ge


@define
class Level:
    """Class representing the level of a tournament"""
    value = field(default=1, validator=[ge(0), instance_of(int)])
    bb = field(default=200.0, validator=[ge(0), instance_of((float, int))])
    ante = field(default=Factory(lambda self: 0.125 * self.bb, takes_self=True),
                 validator=[ge(0), instance_of((float, int))])

    def __str__(self):
        return f"Current level: {self.value}\nAnte={self.ante}\nSB={self.sb}\nBB={self.bb}"

    @property
    def sb(self):
        return self.bb / 2

    def to_json(self):
        level_dict = asdict(self)
        level_dict["sb"] = self.sb
        return level_dict
