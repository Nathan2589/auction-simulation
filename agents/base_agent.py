from abc import ABC, abstractmethod
from simulation.data_models import AuctionState, Bid, AuctionResult

class BaseAgent(ABC):
    def __init__(self, agent_id: int):
        self.agent_id = agent_id

    @abstractmethod
    def get_bid(self, auction_state: AuctionState, history: list[AuctionResult]) -> Bid:
        pass