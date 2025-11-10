from simulation.auction_logic import run_auction
from simulation.data_models import Bid, AuctionResult

bids = [
    Bid(agent_id=1, bid_amount=100.0),
    Bid(agent_id=2, bid_amount=150.0),
    Bid(agent_id=3, bid_amount=120.0),
    Bid(agent_id=4, bid_amount=150.0),
]

def test_run_auction_deterministic_winner():
    auction_id = 1
    random_seed = 42

    result: AuctionResult = run_auction(bids, auction_id, random_seed)

    assert result.auction_id == auction_id
    assert result.winning_agent_id == 2  # With seed 42, agent 2 should win
    assert result.winning_bid == 150.0
    assert len(result.all_bids) == len(bids)
    print(f"Test passed: Deterministic winner with seed {random_seed} is agent {result.winning_agent_id} with bid {result.winning_bid}")

def test_run_auction_no_bids():
    auction_id = 2
    random_seed = 42

    result: AuctionResult = run_auction([], auction_id, random_seed)

    assert result.auction_id == auction_id
    assert result.winning_agent_id == -1
    assert result.winning_bid == 0.0
    assert len(result.all_bids) == 0
    print(f"Test passed: No bids results in no winner: agent_id {result.winning_agent_id}, bid {result.winning_bid}")

def test_run_auction_all_zero_bids():
    auction_id = 3
    random_seed = 42
    zero_bids = [
        Bid(agent_id=1, bid_amount=0.0),
        Bid(agent_id=2, bid_amount=0.0),
    ]

    result: AuctionResult = run_auction(zero_bids, auction_id, random_seed)

    assert result.auction_id == auction_id
    assert result.winning_agent_id == -1
    assert result.winning_bid == 0.0
    assert len(result.all_bids) == len(zero_bids)
    print(f"Test passed: All zero bids results in no winner: agent_id {result.winning_agent_id}, bid {result.winning_bid}")

def test_run_auction_tie_breaker():
    auction_id = 4
    random_seed = 99
    tie_bids = [
        Bid(agent_id=1, bid_amount=200.0),
        Bid(agent_id=2, bid_amount=200.0),
        Bid(agent_id=3, bid_amount=150.0),
    ]

    result: AuctionResult = run_auction(tie_bids, auction_id, random_seed)

    assert result.auction_id == auction_id
    assert result.winning_bid == 200.0
    assert result.winning_agent_id in [1, 2]  # Either agent 1 or 2 can win
    assert len(result.all_bids) == len(tie_bids)
    print(f"Test passed: Tie breaker with seed {random_seed} results in winner agent_id {result.winning_agent_id} with bid {result.winning_bid}")

