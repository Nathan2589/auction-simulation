import agents.llm_agent as llm_agent
import agents.random_agent as random_agent
import pandas as pd
from simulation import auction_environment


def main():
    llm_agents = [llm_agent.LLMAgent(agent_id=i) for i in range(3)]
    random_agents = [random_agent.RandomAgent(agent_id=i+3, random_seed=42+i) for i in range(3)]
    all_agents = llm_agents + random_agents
    env = auction_environment.AuctionEnvironment(auction_id=1, random_seed=100, agents=all_agents)
    num_rounds = 25
    results = env.run_simulation(num_rounds=num_rounds)
    rows = []
    for round_number, result in enumerate(results, start=1):
        for bid in result.all_bids:
            agent_type = "LLM" if bid.agent_id < 3 else "Random"
            private_value = result.private_values.get(bid.agent_id, 0.0)   
            won = bid.agent_id == result.winning_agent_id
            utility = bid.bid_amount - private_value if won else 0.0
            rows.append({
                "round": round_number,
                "agent_id": bid.agent_id,
                "agent_type": agent_type,
                "bid_amount": bid.bid_amount,
                "private_value": private_value,
                "won": won,
                "utility": utility
            })
    df = pd.DataFrame(rows)
    df.to_csv("auction_results.csv", index=False)
    print("Auction simulation completed. Results saved to auction_results.csv")

    print("\nSummary Statistics:")
    print(df.groupby('agent_id')['utility'].sum())
    print(df.groupby('agent_type')['utility'].sum())
            
        
if __name__ == "__main__":
    main()
