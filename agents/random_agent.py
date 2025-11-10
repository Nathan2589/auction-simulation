import agents.base_agent as base_agent
import random
class RandomAgent(base_agent.BaseAgent):
    def get_bid(self, auction_state, history):
        
        bid_amount = random.uniform(0, auction_state.private_value)
        return base_agent.Bid(agent_id=self.agent_id, bid_amount=bid_amount)