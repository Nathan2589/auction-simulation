# statless function

from simulation.data_models import Bid, AuctionResult
import random

def run_auction(bids: list[Bid], auction_id: int, random_seed: int) -> AuctionResult:
    if not bids:
       
        return AuctionResult(
            auction_id=auction_id,
            winning_agent_id=-1,
            winning_bid=0.0,
            all_bids=[],
        )
    
    filtered_bids = [bid for bid in bids if bid.bid_amount > 0]

    if not filtered_bids:
        return AuctionResult(
            auction_id=auction_id,
            winning_agent_id=-1,
            winning_bid=0.0,
            all_bids=bids,
        )
    if random_seed is not None:
        random.seed(random_seed)
    
    highest_bid = max(bid.bid_amount for bid in filtered_bids)
    tied_bids = [bid for bid in filtered_bids if bid.bid_amount == highest_bid]
    winning_bid = random.choice(tied_bids)


    
    return AuctionResult(
        auction_id=auction_id,
        winning_agent_id=winning_bid.agent_id,
        winning_bid=winning_bid.bid_amount,
        all_bids=bids,
    )