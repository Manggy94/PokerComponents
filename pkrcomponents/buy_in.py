from attrs import define, field, asdict
from attrs.validators import instance_of, ge


@define
class BuyIn:
    """Class representing the buy-in of a tournament"""
    prize_pool = field(default=0.0, validator=[ge(0), instance_of((int, float))])
    bounty = field(default=0.0, validator=[ge(0), instance_of((int, float))])
    rake = field(default=0.0, validator=[ge(0), instance_of((int, float))])

    def __str__(self):
        return f"Buy-in: {self.total}"

    @property
    def total(self):
        return self.prize_pool + self.bounty + self.rake

    def to_json(self):
        return asdict(self)
