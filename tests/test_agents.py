from simulation.data_models import Bid, AuctionResult, AuctionState

from agents.random_agent import RandomAgent
import unittest

class TestRandomAgent(unittest.TestCase):
    def setUp(self):
        self.agent = RandomAgent(agent_id=1)
        self.auction_state = AuctionState(
            agent_id=1,
            private_value=100.0,
            round_number=1
        )

    
    def test_bid_within_bounds(self):
        for _ in range(100):
            bid = self.agent.get_bid(self.auction_state, [])
            self.assertGreaterEqual(bid.bid_amount, 0)
            self.assertLessEqual(bid.bid_amount, self.auction_state.private_value)
            self.assertIsInstance(bid, Bid)
    
    def test_bid_contains_correct_metadata(self):
        bid = self.agent.get_bid(self.auction_state, [])
        self.assertEqual(bid.agent_id, self.agent.agent_id)
        