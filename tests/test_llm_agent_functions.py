import unittest
from unittest.mock import patch, MagicMock
from agents.llm_agent import LLMAgent
from simulation.data_models import AuctionState, AuctionResult, Bid
import os
class TestLLMAgent(unittest.TestCase):
    def setUp(self):
        
        self.agent = LLMAgent(agent_id=0, model="test-model")
        mock_response = {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "Reasoning blah blah... \nBID: 50.6"
                }
            ]
        }
        self.agent.client.messages.create = MagicMock(return_value=mock_response)

    def test_get_bid_returns_correct_bid(self):
        auction_state = AuctionState(
            agent_id=0,
            round_number=1,
            private_value=100.0
        )
        history = []
        bid = self.agent.get_bid(auction_state, history)
        self.assertIsInstance(bid, Bid)
        self.assertEqual(bid.agent_id, 0)
        self.assertAlmostEqual(bid.bid_amount, 50.6)