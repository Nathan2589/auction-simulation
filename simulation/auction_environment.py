from simulation.auction_logic import run_auction
from simulation.data_models import Bid, AuctionResult, AgentProfile, AuctionState
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