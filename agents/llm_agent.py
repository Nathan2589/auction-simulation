from simulation.data_models import Bid, AuctionState, AuctionResult
from agents.base_agent import BaseAgent
import anthropic
from dotenv import load_dotenv
import os
import re

load_dotenv()

class LLMAgent(BaseAgent):
    def __init__(self, agent_id: int, model: str = "claude-sonnet-4-20250514"):
        super().__init__(agent_id)
        api_key=os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables.")
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
    
    def _format_prompt(self, auction_state: AuctionState, history: list[AuctionResult]) -> str:
        prompt = f"For this auction round, your private value for the item is: {auction_state.private_value}\n"
        if auction_state.round_number > 1:
            prompt += f"Here is the history of previous auctions:\n"
            for result in history:
                prompt += f"In round {result.round_number}, the winning bid was {result.winning_bid}.\n"
                if result.winning_agent_id == self.agent_id:
                    prompt += f"You bid {result.winning_bid}. Your bid won.\n"
                else:
                    prompt += f"You bid {next(bid.bid_amount for bid in result.all_bids if bid.agent_id == self.agent_id)}. Your bid lost.\n"
                    prompt += f"The winning bid was {result.winning_bid}.\n"
        else:
            prompt += "This is the first auction round, so there is no history.\n"
        prompt += "Based on this information, what is your bid amount for this auction round?\n"
        prompt += "Output your reasoning first, then on a new line provide your bid amount in the format: BID: <amount>\n"
        print(f"Formatted prompt: {prompt}")
        return prompt
    
    def _parse_bid_from_response(self, response: dict) -> float:
        text = ""
        if isinstance(response, dict):
            content = response.get("content")
            if isinstance(content, list):
                parts = []
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        parts.append(item.get("text", ""))
                text = "".join(parts).strip()
        # fallback to string conversion
        if not text:
            text = str(response)

        match = re.search(r'BID\s*[:\-]\s*([0-9]+(?:\.[0-9]+)?)', text, re.IGNORECASE)
        if match:
            return float(match.group(1))
        
        raise ValueError("Could not parse bid amount from LLM response.")

        

    
    def get_bid(self, auction_state: AuctionState, history: list[AuctionResult]) -> Bid:
        prompt = self._format_prompt(auction_state, history)

        response = self.client.messages.create(
            model= self.model,
            max_tokens=500,
            system="You are a strategic bidder in a first-price sealed-bid auction.\nIf you win, you pay your bid amount. Your goal is to maximise your profit over multiple rounds.\n",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        print(f"LLM Response: {response}")
        bid_amount = self._parse_bid_from_response(response)
        return Bid(agent_id=self.agent_id, bid_amount=bid_amount)
        
