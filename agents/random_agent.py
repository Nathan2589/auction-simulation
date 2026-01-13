import agents.base_agent as base_agent
from simulation.data_models import ItemBid, MultiItemAuctionState, MultiItemAuctionResult
import random


class RandomAgent(base_agent.BaseAgent):
    def __init__(self, agent_id: int, random_seed: int = None):
        super().__init__(agent_id)
        self.rng = random.Random(random_seed)

    def get_bid(self, auction_state, history):
        bid_amount = self.rng.uniform(0, auction_state.private_value)
        return base_agent.Bid(agent_id=self.agent_id, bid_amount=bid_amount)

    def get_item_bids(
        self,
        auction_state: MultiItemAuctionState,
        history: list[MultiItemAuctionResult]
    ) -> list[ItemBid]:
        """Bid randomly on each item up to private value."""
        bids = []
        for item in auction_state.items:
            private_value = auction_state.private_values.get(item.item_id, 0)
            bid_amount = self.rng.uniform(0, private_value)
            bids.append(ItemBid(
                agent_id=self.agent_id,
                item_id=item.item_id,
                bid_amount=bid_amount
            ))
        return bids