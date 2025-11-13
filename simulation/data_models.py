from dataclasses import dataclass, field


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
    round_number: int
    winning_bid: float
    all_bids: list[Bid]
    private_values: dict[int, float] = field(default_factory=dict)  # Optional, defaults to empty dict