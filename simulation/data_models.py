from dataclasses import dataclass
from typing import Optional

@dataclass
class AgentProfile:
    agent_id: int


@dataclass 
class Bid:
    agent_id: int
    bid_amount: float


@dataclass 
class AuctionResult:
    auction_id: int
    winning_agent_id: int
    winning_bid: float
    all_bids: list[Bid]