from simulation.auction_environment import AuctionEnvironment
from simulation.data_models import Bid, AuctionResult, AuctionState
from agents.random_agent import RandomAgent
import unittest

class TestAuctionEnvironment(unittest.TestCase):
    def test_simulation_completes_with_correct_rounds(self):
        agents = [RandomAgent(agent_id=i) for i in range(3)]
        env = AuctionEnvironment(auction_id=1, random_seed=42, agents=agents)
        num_rounds = 5
        results = env.run_simulation(num_rounds=num_rounds)
        self.assertEqual(len(results), num_rounds)
    
    def test_each_round_has_correct_number_of_bids(self):
        agents = [RandomAgent(agent_id=i) for i in range(3)]
        env = AuctionEnvironment(auction_id=1, random_seed=99, agents=agents)
        num_round = 5
        results = env.run_simulation(num_rounds=num_round)
        for result in results:
            self.assertEqual(len(result.all_bids), len(agents))

        
    def test_reproducibility_with_random_seed(self):
        base_seed = 123
        agents1 = [RandomAgent(agent_id=i, random_seed=base_seed+i) for i in range(3)]
        agents2 = [RandomAgent(agent_id=i, random_seed=base_seed+i) for i in range(3)]
        env1 = AuctionEnvironment(auction_id=1, random_seed=base_seed, agents=agents1)
        env2 = AuctionEnvironment(auction_id=1, random_seed=base_seed, agents=agents2)
        num_rounds = 4
        results1 = env1.run_simulation(num_rounds=num_rounds)
        print(f"results1: {[res.winning_agent_id for res in results1]}")
        results2 = env2.run_simulation(num_rounds=num_rounds)
        print(f"results2: {[res.winning_agent_id for res in results2]}")
        for res1, res2 in zip(results1, results2):
            self.assertEqual(res1.winning_agent_id, res2.winning_agent_id)
            self.assertEqual(res1.winning_bid, res2.winning_bid)
    
    def test_history_is_passed_to_agents(self):
        class SpyAgent(RandomAgent):
            def __init__(self, agent_id: int):
                super().__init__(agent_id)
                self.received_history_in_round = {}

            def get_bid(self, auction_state: AuctionState, history: list[AuctionResult]) -> Bid:
                print(f"Round {auction_state.round_number}: Agent {self.agent_id} received history with {len(history)} items")
                self.received_history_in_round[auction_state.round_number] = len(history)
                return super().get_bid(auction_state, history)
        
        agents = [SpyAgent(agent_id=i) for i in range(2)]
        env = AuctionEnvironment(auction_id=1, random_seed=50, agents=agents)
        num_rounds = 3
        env.run_simulation(num_rounds=num_rounds)
        for round_number in range(1, num_rounds + 1):
            for agent in agents:
                received_history = agent.received_history_in_round.get(round_number, [])
                self.assertEqual(received_history, round_number - 1)
        
