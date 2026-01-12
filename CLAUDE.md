# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a first-price sealed-bid auction simulation that pits LLM-powered agents against random bidding agents. The simulation runs multiple rounds where agents bid based on private values, and the highest bidder wins (paying their bid amount).

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the simulation
python main.py

# Run all tests
pytest

# Run a single test file
pytest tests/test_agents.py

# Run a specific test
pytest tests/test_agents.py::TestRandomAgent::test_bid_within_bounds
```

## Architecture

### Core Components

**Simulation Layer** (`simulation/`)
- `data_models.py` - Dataclasses for `Bid`, `AuctionState`, `AuctionResult`, `AgentProfile`
- `auction_logic.py` - Stateless `run_auction()` function that determines winners with deterministic tie-breaking
- `auction_environment.py` - `AuctionEnvironment` orchestrates multi-round simulations, manages RNG for reproducibility

**Agent Layer** (`agents/`)
- `base_agent.py` - Abstract `BaseAgent` with `get_bid(auction_state, history)` interface
- `llm_agent.py` - `LLMAgent` uses Anthropic API to make bidding decisions
- `random_agent.py` - `RandomAgent` bids uniformly random up to private value

### Data Flow

1. `AuctionEnvironment._setup_round()` generates private values for each agent
2. Each agent receives `AuctionState` (private value, round number) and bid history
3. `run_auction()` collects bids, filters zeros, selects highest bidder (random tie-break)
4. Results tracked per-round with `AuctionResult` including all bids and private values

### Environment Variables

The LLM agent requires `ANTHROPIC_API_KEY` in `.env` file.
