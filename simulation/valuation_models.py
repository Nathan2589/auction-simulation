from abc import ABC, abstractmethod
from itertools import combinations


class ValuationModel(ABC):
    """Abstract base class for computing bundle valuations."""

    @abstractmethod
    def get_bundle_value(
        self, bundle: frozenset[int], base_values: dict[int, float]
    ) -> float:
        """
        Compute the value of a bundle given base item values.

        Args:
            bundle: Set of item IDs in the bundle.
            base_values: Mapping of item_id -> base value for that item.

        Returns:
            Total value of the bundle under this valuation model.
        """
        pass


class AdditiveValuation(ValuationModel):
    def get_bundle_value(
        self, bundle: frozenset[int], base_values: dict[int, float]
    ) -> float:
        return sum(base_values.get(item_id, 0.0) for item_id in bundle)


class SynergyValuation(ValuationModel):
    """
    Synergy valuation: v(AB) = v(A) + v(B) + synergy_bonus.

    Complementary items are worth more together than separately.
    Only pairwise synergies are supported.
    """

    def __init__(self, synergies: dict[frozenset[int], float]):
        """
        Args:
            synergies: Mapping of item pairs (as frozensets) to bonus values.
                       Example: {frozenset({0, 1}): 10.0} means items 0 and 1
                       together add a bonus of 10.0.
        """
        
        for pair, bonus in synergies.items():
            if len(pair) != 2:
                raise ValueError(f"Synergies must be pairwise, got {pair}")
            if bonus < 0:
                raise ValueError(f"Synergy bonus must be non-negative, got {bonus}")
        self.synergies = synergies

    def get_bundle_value(
        self, bundle: frozenset[int], base_values: dict[int, float]
    ) -> float:
        
        total = sum(base_values.get(item_id, 0.0) for item_id in bundle)

        
        for pair, bonus in self.synergies.items():
            if pair.issubset(bundle):
                total += bonus

        return total


class SubstitutesValuation(ValuationModel):
    """
    Substitutes valuation: within each substitute group, only the max value counts.

    For items that serve the same purpose, you only need one.
    """

    def __init__(self, substitute_groups: list[frozenset[int]]):
        """
        Args:
            substitute_groups: List of item groups where items are substitutes.
                               Example: [frozenset({0, 1})] means items 0 and 1
                               are substitutes (only max value counts).
        """
        self.substitute_groups = substitute_groups

    def get_bundle_value(
        self, bundle: frozenset[int], base_values: dict[int, float]
    ) -> float:
        # Track which items have been accounted for via substitute groups
        accounted_items = set()
        total = 0.0

        # For each substitute group, take max value of items in bundle
        for group in self.substitute_groups:
            items_in_bundle = group.intersection(bundle)
            if items_in_bundle:
                max_value = max(
                    base_values.get(item_id, 0.0) for item_id in items_in_bundle
                )
                total += max_value
                accounted_items.update(items_in_bundle)

        # Add values for items not in any substitute group
        for item_id in bundle:
            if item_id not in accounted_items:
                total += base_values.get(item_id, 0.0)

        return total
