import os 
import unittest
from agents.llm_agent import LLMAgent
from simulation.data_models import AuctionState, Bid


HAS_KEY = bool(os.getenv("ANTHROPIC_API_KEY"))
@unittest.skipUnless(HAS_KEY, "ANTHROPIC_API_KEY not set in environment variables.")
class TestLLMIntegration(unittest.TestCase):
    def setUp(self):
        self.agent = LLMAgent(agent_id=0, model=os.getenv("TEST_LLM_MODEL", "claude-sonnet-4-20250514"))

    def test_llm_agent_get_bid(self):
        state = AuctionState(
            agent_id=0,
            round_number=1,
            private_value=100.0
        )
        bid = self.agent.get_bid(state, history=[])
        self.assertIsInstance(bid, Bid)
        self.assertEqual(bid.agent_id, 0)
        self.assertGreaterEqual(bid.bid_amount, 0.0)
        self.assertLessEqual(bid.bid_amount, state.private_value)  # Bid should not exceed private value