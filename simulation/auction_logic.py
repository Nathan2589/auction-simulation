# stateless functions

from simulation.data_models import Bid, AuctionResult, ItemBid, MultiItemAuctionResult, Item
import random
from collections import defaultdict

def run_auction(bids: list[Bid], auction_id: int, rng: random.Random | None = None, round_number: int = 0) -> AuctionResult:

    if rng is None:
        rng = random.Random()

    if not bids:
       
        return AuctionResult(
            auction_id=auction_id,
            winning_agent_id=-1,
            winning_bid=0.0,
            all_bids=[],
            round_number=round_number
        )
    
    filtered_bids = [bid for bid in bids if bid.bid_amount > 0]

    if not filtered_bids:
        return AuctionResult(
            auction_id=auction_id,
            winning_agent_id=-1,
            winning_bid=0.0,
            all_bids=bids,
            round_number=round_number
        )
    
    
    highest_bid = max(bid.bid_amount for bid in filtered_bids)
    tied_bids = [bid for bid in filtered_bids if bid.bid_amount == highest_bid]
    # Use provided RNG rather than global random to maintain determinism
    winning_bid = rng.choice(tied_bids)


    
    return AuctionResult(
        auction_id=auction_id,
        winning_agent_id=winning_bid.agent_id,
        winning_bid=winning_bid.bid_amount,
        all_bids=bids,
        round_number=round_number
    )


def run_multi_item_auction(
    bids: list[ItemBid],
    items: list[Item],
    auction_id: int,
    rng: random.Random | None = None,
    round_number: int = 0
) -> MultiItemAuctionResult:
    """
    Run independent first-price sealed-bid auctions for each item.
    Each item is allocated to the highest bidder for that item.
    """
    if rng is None:
        rng = random.Random()

    # Group bids by item
    bids_by_item: dict[int, list[ItemBid]] = defaultdict(list)
    for bid in bids:
        bids_by_item[bid.item_id].append(bid)

    allocations: dict[int, int] = {}
    prices: dict[int, float] = {}

    for item in items:
        item_bids = bids_by_item.get(item.item_id, [])
        filtered_bids = [b for b in item_bids if b.bid_amount > 0]

        if not filtered_bids:
            allocations[item.item_id] = -1
            prices[item.item_id] = 0.0
            continue

        highest_bid = max(b.bid_amount for b in filtered_bids)
        tied_bids = [b for b in filtered_bids if b.bid_amount == highest_bid]
        winner = rng.choice(tied_bids)

        allocations[item.item_id] = winner.agent_id
        prices[item.item_id] = winner.bid_amount

    return MultiItemAuctionResult(
        auction_id=auction_id,
        round_number=round_number,
        allocations=allocations,
        prices=prices,
        all_bids=bids
    )