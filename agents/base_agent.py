from abc import ABC, abstractmethod
from simulation.data_models import (
    AuctionState, Bid, AuctionResult,
    MultiItemAuctionState, ItemBid, MultiItemAuctionResult
)


class BaseAgent(ABC):
    def __init__(self, agent_id: int):
        self.agent_id = agent_id

    @abstractmethod
    def get_bid(self, auction_state: AuctionState, history: list[AuctionResult]) -> Bid:
        """Return a bid for a single-item auction."""
        pass

    def get_item_bids(
        self,
        auction_state: MultiItemAuctionState,
        history: list[MultiItemAuctionResult]
    ) -> list[ItemBid]:
        """Return bids for a multi-item auction. Override in subclasses."""
        raise NotImplementedError(
            f"{self.__class__.__name__} does not support multi-item auctions"
        )