from attrs import define, field, asdict
from attrs.validators import instance_of, ge


@define
class BuyIn:
    """
    This class represents the buy-in of a poker tournament

    Attributes:
        prize_pool(float): The prize pool of the tournament
        bounty(float): The bounty of the tournament
        rake(float): The rake of the tournament

    Methods:
        __str__(): Returns a string representation of the buy-in
        to_json(): Returns a json representation of the buy-in

    Properties:
        total(float): Returns the total value of the buy-in

    """
    prize_pool = field(default=0.0, validator=[ge(0), instance_of((int, float))])
    bounty = field(default=0.0, validator=[ge(0), instance_of((int, float))])
    rake = field(default=0.0, validator=[ge(0), instance_of((int, float))])

    def __str__(self):
        return f"Buy-in: {self.total}"

    @property
    def total(self) -> float:
        """
        Returns the total value of the buy-in

        Returns:
            float: The total value of the buy-in
        """
        return self.prize_pool + self.bounty + self.rake

    def to_json(self) -> dict:
        """
        Returns a json representation of the buy-in

        Returns:
            json_dicct (dict): A json representation of the buy-in
        """
        return asdict(self)
