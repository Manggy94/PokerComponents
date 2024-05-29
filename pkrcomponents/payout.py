from attrs import define, field, asdict
from attrs.validators import instance_of, ge


@define
class Payout:
    """
    This class represents a payout in a poker tournament

    Attributes:
        tier(int): The tier of the payout
        reward(float): The reward of the payout

    Methods:
        __str__(): Returns a string representation of the payout
        to_json(): Returns a json representation of the payout
    """
    tier = field(default=1, validator=[ge(0), instance_of(int)])
    reward = field(default=0.0, validator=[ge(0), instance_of((int, float))])

    def __str__(self) -> str:
        """
        Returns a string representation of the payout

        Returns:
            str: A string representation of the payout
        """
        return f"Tier: {self.tier} - Reward: {self.reward}"

    def to_json(self) -> dict:
        """
        Returns a json representation of the payout

        Returns:
            dict: A json representation of the payout
        """
        return asdict(self)


class Payouts(list):
    """
    This class represents a list of payouts in a poker tournament

    Methods:
        add_payout(payout: Payout): Add a payout to the list
        remove_payout(tier: int): Remove a payout from the list
        get_payout(rank: int) -> Payout: Get the reward for a given finish rank
        closest_payout(rank: int) -> Payout: Get the closest payout to a given rank
        get_reward(rank: int) -> float: Get the reward for a given finish rank
        get_prize_pool() -> float: Get the total prize pool distributed via the payouts
    """

    def add_payout(self, payout: Payout) -> None:
        """
        A method to add a payout to the list

        Args:
            payout (Payout): The payout to add
        """
        self.append(payout)

    def remove_payout(self, tier: int) -> None:
        """
        A method to remove a payout from the list

        Args:
            tier (int): The tier of the payout to remove
        """
        for payout in self:
            if payout.tier == tier:
                self.remove(payout)



    def get_payout(self, rank: int) -> Payout:
        """
        A method to get the reward for a given finish rank

        Args:
            rank (int): The rank of the player

        Returns:
            Payout: The payout for the given rank
        """
        for tier, reward in zip(self.tiers, self.rewards):
            if tier >= rank:
                return Payout(tier, reward)
        return Payout(0, 0.0)

    def closest_payout(self, rank: int) -> Payout:
        """
        A method to get the closest payout to a given rank

        Args:
            rank (int): The rank of the player

        Returns:
            Payout: The closest payout to the given rank
        """
        i = 0
        while i < len(self) and rank > self[i].tier:
            i += 1
        return self[i-1]

    def get_reward(self, rank: int) -> float:
        """
        A method to get the reward for a given finish rank

        Args:
            rank (int): The rank of the player

        Returns:
            float: The reward for the given rank
        """
        return self.get_payout(rank).reward

    def get_prize_pool(self) -> float:
        """
        A method to get the total prize pool distributed via the payouts

        Returns:
            float: The total prize pool distributed via the payouts
        """
        return sum(self.get_reward(rank) for rank in range(1, max(self.tiers)+1))

    @property
    def tiers(self) -> list:
        """
        A property to get the tiers of the payouts
        """
        return [payout.tier for payout in self]

    @property
    def rewards(self) -> list:
        """
        A property to get the rewards of the payouts
        """
        return [payout.reward for payout in self]
