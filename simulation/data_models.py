from dataclasses import dataclass


@dataclass
class AgentProfile:
    agent_id: int


@dataclass 
class Bid:
    agent_id: int
    bid_amount: float

@dataclass
class AuctionState:
    agent_id: int
    private_value: float
    round_number: int

@dataclass 
class AuctionResult:
    auction_id: int
    winning_agent_id: int
    winning_bid: float
    all_bids: list[Bid]