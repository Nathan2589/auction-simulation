import agents.base_agent as base_agent
from simulation.data_models import AuctionState, Bid
import anthropic

class LLMAgent(base_agent.BaseAgent):
    def __init__(self, agent_id: int):
        super().__init__(agent_id)
        self.client = anthropic.Anthropic()
        self.model = "claude-sonnet-4-5-20250929" #model name

    
    def _format_prompt(self, auction_state: AuctionState, history: list[AuctionState]) -> str:
        prompt = f"You are a strategic bidder in an auction. Your private value for the item is {auction_state.private_value:.2f}.\n"
        prompt += "The rules are first-price sealed-bid auction: the highest bid wins and pays their bid amount. Your goal is to maximize profit.\n"

