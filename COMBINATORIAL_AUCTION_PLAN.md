# Combinatorial Auction Extension Plan

## Overview

Extend the auction simulation to support **combinatorial auctions** where LLM agents bid on bundles of items with synergies/complementarities. This tests whether LLMs can reason about complex valuations and develop strategic bidding behavior in computationally challenging auction formats.

## Research Questions

- Can LLMs correctly identify and exploit item synergies?
- Do LLMs learn to shade bids appropriately in first-price combinatorial auctions?
- How does LLM performance compare to random agents in terms of allocative efficiency and profit?
- Do different auction formats (first-price vs VCG) affect LLM bidding behavior?

---

## Phase 1: Multi-Item Infrastructure

**Goal**: Support multiple items per auction (independent valuations, no bundles yet)

**Files to modify**:
- `simulation/data_models.py` - Add `Item`, `MultiItemAuctionState`, `ItemBid`, `MultiItemAuctionResult`
- `simulation/auction_environment.py` - Generate per-item private values, collect per-item bids
- `agents/base_agent.py` - Add `get_item_bids()` returning `list[ItemBid]`
- `agents/random_agent.py` - Extend RandomAgent class to include get_item_bids() -> `list[ItemBid]`

**Testing**: Run with 3-5 items, verify each allocated independently

---

## Phase 2: Valuation Models

**Goal**: Model synergies (complementary items) and substitutes

**Files to create**:
- `simulation/valuation_models.py` - Abstract `ValuationModel` with implementations:
  - `AdditiveValuation` - v(AB) = v(A) + v(B)
  - `SynergyValuation` - v(AB) = v(A) + v(B) + synergy_bonus
  - `SubstitutesValuation` - v(AB) = max(v(A), v(B))

**Files to modify**:
- `simulation/auction_environment.py` - Accept `ValuationModel`, generate synergy matrices

**Testing**: Unit tests verifying bundle value computations

---

## Phase 3: Bundle Bidding

**Goal**: Agents submit XOR bids on bundles (win at most one)

**Files to modify**:
- `simulation/data_models.py` - Add `BundleBid(agent_id, bundle: frozenset[int], amount)`, `XORBidCollection`
- `agents/base_agent.py` - Add `get_bundle_bids()` method
- `agents/random_agent.py` - Implement `RandomBundleAgent` (samples random bundles, bids fraction of value)

**Testing**: Verify XOR constraint enforcement, bid validation

---

## Phase 4: Winner Determination

**Goal**: Solve combinatorial allocation optimally

**Files to create**:
- `simulation/winner_determination.py` - `ILPWinnerDetermination` using PuLP, `GreedyWinnerDetermination` as fallback
- `simulation/payment_rules.py` - `FirstPricePayment`, `VCGPayment`

**Files to modify**:
- `simulation/auction_logic.py` - Add `run_combinatorial_auction()` calling WDP solver

**Dependencies**: Add `pulp` to requirements.txt

**Complexity constraints**: Limit to ~10 items, ~20 bundles/agent, 30s solver timeout

**Testing**: Small instances with known optimal solutions

---

## Phase 5: LLM Integration

**Goal**: Restructure prompts for bundle reasoning

**Files to modify**:
- `agents/llm_agent.py` - Create `CombinatorialLLMAgent` with two-phase prompting:
  1. **Valuation phase**: Given items + synergies, compute bundle values
  2. **Bidding phase**: Given values + history, submit strategic XOR bids

**Prompt format**:
```
BID: bundle=[1,2] amount=45.5
BID: bundle=[3] amount=30.0
```

**Parsing**: Regex extraction with validation, consider Anthropic structured output

**Testing**: Mock API tests, parsing edge cases, live integration with small instances

---

## Phase 6: Analysis & Visualization

**Goal**: Metrics for evaluating LLM performance

**Files to create**:
- `analysis/metrics.py` - `AuctionAnalyzer` computing:
  - Allocative efficiency (actual vs optimal welfare)
  - Agent win rates, profit, bid shading
  - Synergy exploitation rate
- `analysis/visualization.py` - Learning curves, bid distributions, efficiency plots

**Files to modify**:
- `main.py` - Integrate analysis pipeline, export results

**Dependencies**: Add `matplotlib`, `seaborn` to requirements.txt

---

## Critical Files Summary

| File | Changes |
|------|---------|
| `simulation/data_models.py` | Add Item, BundleBid, XORBidCollection, CombinatorialAuctionResult |
| `simulation/auction_logic.py` | Add run_combinatorial_auction() |
| `simulation/auction_environment.py` | Multi-item setup, valuation model integration |
| `agents/base_agent.py` | Add get_bundle_bids() abstract method |
| `agents/llm_agent.py` | CombinatorialLLMAgent with bundle prompts |
| `simulation/valuation_models.py` | NEW: ValuationModel hierarchy |
| `simulation/winner_determination.py` | NEW: ILP and greedy WDP solvers |
| `simulation/payment_rules.py` | NEW: First-price and VCG payment rules |
| `analysis/metrics.py` | NEW: Efficiency and agent metrics |

---

## Verification Plan

After each phase:
1. Run `pytest` to ensure no regressions
2. Phase 4+: Run small combinatorial auction (3 items, 2 agents, 5 rounds)
3. Phase 5+: Verify LLM responses parse correctly
4. Phase 6: Generate analysis report comparing LLM vs random agents

**End-to-end test**:
```bash
python main.py  # Should run 5-item combinatorial auction with 2 LLM + 2 random agents
# Outputs: auction_results.csv, efficiency metrics, learning curve plots
```

---

## Dependencies to Add

```
# requirements.txt
pulp>=2.7
matplotlib>=3.7
seaborn>=0.12
```

---

## Background: Combinatorial Auction Theory

### Why Combinatorial Auctions?

In standard single-item auctions, agents bid on one item at a time. But many real-world scenarios involve **complementary goods**:
- Spectrum licenses (adjacent frequencies are more valuable together)
- Airport landing slots (arrival + departure slots at same airport)
- Advertising packages (multiple ad placements for campaign reach)

### Key Concepts

**Synergies/Complementarities**: Items worth more together than separately
- Example: v({A,B}) > v({A}) + v({B})

**Substitutes**: Items that serve similar purposes
- Example: v({A,B}) < v({A}) + v({B})

**XOR Bidding**: Agent submits multiple bundle bids but wins at most one
- Prevents "exposure problem" (winning partial bundle)

**Winner Determination Problem (WDP)**: Finding optimal allocation is NP-hard
- Must decide which bids to accept to maximize total value
- Items can only be allocated once

### Auction Formats

**First-Price**: Winners pay their bids
- Strategic complexity: bid below value to profit
- Revenue depends on competition

**VCG (Vickrey-Clarke-Groves)**: Winners pay "opportunity cost"
- Truthful bidding is dominant strategy
- Lower revenue but better efficiency guarantees

---

## Game-Theoretic Research Value

This extension enables studying:

1. **Strategic Reasoning**: Do LLMs understand bid shading in first-price formats?
2. **Truthfulness**: Do LLMs bid truthfully in VCG (where it's optimal)?
3. **Bundle Optimization**: Can LLMs identify high-value bundles?
4. **Learning**: Do LLMs adapt strategy based on competitor behavior?
5. **Emergent Behavior**: Do multiple LLMs develop "collusive-like" patterns?
