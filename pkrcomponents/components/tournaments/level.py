import attrs
from attrs import define, field, Factory, asdict
from attrs.validators import instance_of, ge


@define
class Level:
    """
    This class represents a level in a poker tournament

    Attributes:
        value(int): The value of the level
        bb(float): The big blind of the level
        ante(float): The ante of the level

    Methods:
        __str__(): Returns a string representation of the level
        to_json(): Returns a json representation of the level

    Properties:
        sb(float): Returns the small blind of the level
    """
    value = field(default=1, validator=[ge(0), instance_of(int)])
    bb = field(default=200.0, validator=[ge(0), instance_of((float, int))])
    sb = field(default=Factory(lambda self: self.bb / 2, takes_self=True), validator=[ge(0), instance_of((float, int))])
    ante = field(default=Factory(lambda self: 0.125 * self.bb, takes_self=True),
                 validator=[ge(0), instance_of((float, int))])

    def __str__(self) -> str:
        """
        Returns a string representation of the level

        Returns:
            str: A string representation of the level
        """
        return f"Current level: {self.value}\nAnte={self.ante}\nSB={self.sb}\nBB={self.bb}"

    def to_json(self) -> dict:
        """
        Returns a json representation of the level

        Returns:
            dict: A json representation of the level
        """
        level_dict = asdict(self)
        level_dict["sb"] = self.sb
        return level_dict
