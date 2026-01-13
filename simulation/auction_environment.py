from simulation.auction_logic import run_auction, run_multi_item_auction
from simulation.data_models import (
    Bid, AuctionResult, AgentProfile, AuctionState,
    Item, ItemBid, MultiItemAuctionState, MultiItemAuctionResult
)
from agents.base_agent import BaseAgent
import random
class AuctionEnvironment:
    def __init__(self, auction_id: int, random_seed: int = None, agents: list[BaseAgent] = None):
        self.auction_id = auction_id
        self.auction_rng = random.Random(random_seed) #tie-breaking RNG
        self.value_rng = random.Random(random_seed)   #private value RNG
        self.agents: list[BaseAgent] = agents if agents is not None else []
        
        
        

    def conduct_auction(self, current_round_bids: list[Bid], round_auction_state: list[AuctionState], round_number: int) -> AuctionResult:
        result = run_auction(current_round_bids, self.auction_id, self.auction_rng, round_number=round_number)
        private_values = {state.agent_id: state.private_value for state in round_auction_state}
        result.private_values = private_values
        return result
    
    def _setup_round(self, round_number: int):
        round_auction_state = []
        for agent in self.agents:
            private_value = self.value_rng.uniform(0, 100)  
            state = AuctionState(
                agent_id=agent.agent_id,
                private_value=private_value,
                round_number=round_number
            )
            round_auction_state.append(state)
        return round_auction_state

    def _play_round(self, round_number: int, round_auction_state: list[AuctionState], simulation_results: list[AuctionResult]) -> list[Bid]:
        bids = []
        for agent in self.agents:
            state = next((s for s in round_auction_state if s.agent_id == agent.agent_id and s.round_number == round_number), None)
            bid = agent.get_bid(state, simulation_results)
            bids.append(bid)
        return bids
    

    def run_simulation(self, num_rounds: int):
        simulation_results = []
        for round_number in range(1, num_rounds + 1):
            round_auction_state = self._setup_round(round_number)
            current_round_bids = self._play_round(round_number, round_auction_state, simulation_results)
            result = self.conduct_auction(current_round_bids, round_auction_state, round_number=round_number)
            simulation_results.append(result)
        return simulation_results


class MultiItemAuctionEnvironment:
    """Environment for multi-item auctions where agents bid on multiple items independently."""

    def __init__(
        self,
        auction_id: int,
        items: list[Item],
        agents: list[BaseAgent],
        random_seed: int = None
    ):
        self.auction_id = auction_id
        self.items = items
        self.agents = agents
        self.auction_rng = random.Random(random_seed)
        self.value_rng = random.Random(random_seed)

    def _setup_round(self, round_number: int) -> list[MultiItemAuctionState]:
        """Generate private values for each agent for each item."""
        round_states = []
        for agent in self.agents:
            private_values = {
                item.item_id: self.value_rng.uniform(0, 100)
                for item in self.items
            }
            state = MultiItemAuctionState(
                agent_id=agent.agent_id,
                round_number=round_number,
                items=self.items,
                private_values=private_values
            )
            round_states.append(state)
        return round_states

    def _play_round(
        self,
        round_number: int,
        round_states: list[MultiItemAuctionState],
        history: list[MultiItemAuctionResult]
    ) -> list[ItemBid]:
        """Collect bids from all agents for all items."""
        all_bids = []
        for agent in self.agents:
            state = next(
                (s for s in round_states if s.agent_id == agent.agent_id),
                None
            )
            if state is None:
                continue
            agent_bids = agent.get_item_bids(state, history)
            all_bids.extend(agent_bids)
        return all_bids

    def _conduct_auction(
        self,
        bids: list[ItemBid],
        round_states: list[MultiItemAuctionState],
        round_number: int
    ) -> MultiItemAuctionResult:
        """Run the multi-item auction and return results."""
        result = run_multi_item_auction(
            bids=bids,
            items=self.items,
            auction_id=self.auction_id,
            rng=self.auction_rng,
            round_number=round_number
        )
        # Attach private values for analytics
        result.private_values = {
            state.agent_id: state.private_values
            for state in round_states
        }
        return result

    def run_simulation(self, num_rounds: int) -> list[MultiItemAuctionResult]:
        """Run the full simulation for the specified number of rounds."""
        results = []
        for round_number in range(1, num_rounds + 1):
            round_states = self._setup_round(round_number)
            bids = self._play_round(round_number, round_states, results)
            result = self._conduct_auction(bids, round_states, round_number)
            results.append(result)
        return results