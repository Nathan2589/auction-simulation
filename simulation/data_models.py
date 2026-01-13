from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simulation.valuation_models import ValuationModel


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


# Multi-item auction data models

@dataclass
class Item:
    item_id: int
    name: str = ""

    def __post_init__(self):
        if not self.name:
            self.name = f"Item_{self.item_id}"


@dataclass
class ItemBid:
    agent_id: int
    item_id: int
    bid_amount: float


@dataclass
class MultiItemAuctionState:
    agent_id: int
    round_number: int
    items: list[Item]
    private_values: dict[int, float]  # item_id -> base value
    valuation_model: ValuationModel | None = None  # for computing bundle values


@dataclass
class MultiItemAuctionResult:
    auction_id: int
    round_number: int
    allocations: dict[int, int]  # item_id -> winning_agent_id (-1 if unallocated)
    prices: dict[int, float]  # item_id -> price paid
    all_bids: list[ItemBid]
    private_values: dict[int, dict[int, float]] = field(default_factory=dict)  # agent_id -> {item_id: value}