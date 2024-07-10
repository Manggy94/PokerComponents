import unittest
from pkrcomponents.components.tournaments.payout import Payout, Payouts


class PayoutTest(unittest.TestCase):

    def setUp(self):
        self.payout = Payout(1, 100.0)

    def test_test_invalid_tier_raises_error(self):
        with self.assertRaises(ValueError):
            self.payout.tier = -1

    def test_test_invalid_reward_raises_error(self):
        with self.assertRaises(ValueError):
            self.payout.reward = -1
        with self.assertRaises(TypeError or ValueError):
            self.payout.reward = "text"

    def test_test_valid_tier_sets_correctly(self):
        self.payout.tier = 2
        self.assertEqual(self.payout.tier, 2)

    def test_test_valid_reward_sets_correctly(self):
        self.payout.reward = 200.0
        self.assertEqual(self.payout.reward, 200.0)

    def test_test_str(self):
        self.assertIsInstance(self.payout.__str__(), str)
        self.assertEqual(self.payout.__str__(), "Tier: 1 - Reward: 100.0")

    def test_test_to_json(self):
        self.assertIsInstance(self.payout.to_json(), dict)
        self.assertEqual(self.payout.to_json(), {"tier": 1, "reward": 100.0})


class PayoutsTest(unittest.TestCase):

    def setUp(self):
        self.payouts = Payouts([Payout(1, 300.0), Payout(2, 200.0), Payout(3, 100.0)])

    def test_adding_payout_increases_length(self):
        initial_length = len(self.payouts)
        self.payouts.add_payout(Payout(4, 50.0))
        self.assertEqual(len(self.payouts), initial_length + 1)

    def test_removing_existing_payout_decreases_length(self):
        initial_length = len(self.payouts)
        self.payouts.remove_payout(3)
        self.assertEqual(len(self.payouts), initial_length - 1)

    def test_removing_non_existing_payout_keeps_length(self):
        initial_length = len(self.payouts)
        self.payouts.remove_payout(5)
        self.assertEqual(len(self.payouts), initial_length)

    def test_get_existing_payout_returns_correct_payout(self):
        payout = self.payouts.get_payout(1)
        self.assertEqual(payout.reward, 300.0)

    def test_get_non_existing_payout_returns_zero_payout(self):
        payout = self.payouts.get_payout(5)
        self.assertEqual(payout.reward, 0.0)

    def test_closest_payout_returns_correct_payout(self):
        payout = self.payouts.closest_payout(2)
        self.assertEqual(payout.reward, 300.0)

    def test_get_reward_returns_correct_reward(self):
        reward = self.payouts.get_reward(1)
        self.assertEqual(reward, 300.0)

    def test_get_prize_pool_returns_correct_sum(self):
        prize_pool = self.payouts.get_prize_pool()
        self.assertEqual(prize_pool, 600.0)

    def test_tiers_property_returns_correct_tiers(self):
        tiers = self.payouts.tiers
        self.assertEqual(tiers, [1, 2, 3])

    def test_rewards_property_returns_correct_rewards(self):
        rewards = self.payouts.rewards
        self.assertEqual(rewards, [300.0, 200.0, 100.0])
