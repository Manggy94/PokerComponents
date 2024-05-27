from attrs import define, field, asdict
from attrs.validators import instance_of, ge


@define
class Payout:
    """Class representing the payout of a tournament"""
    tier = field(default=1, validator=[ge(0), instance_of(int)])
    reward = field(default=0.0, validator=[ge(0), instance_of((int, float))])

    def __str__(self):
        return f"Tier: {self.tier} - Reward: {self.reward}"

    def to_json(self):
        return asdict(self)


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
