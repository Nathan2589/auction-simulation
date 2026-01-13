import unittest
from simulation.valuation_models import (
    AdditiveValuation,
    SynergyValuation,
    SubstitutesValuation,
)


class TestAdditiveValuation(unittest.TestCase):
    def setUp(self):
        self.valuation = AdditiveValuation()
        self.base_values = {0: 10.0, 1: 20.0, 2: 30.0, 3: 40.0}

    def test_empty_bundle(self):
        value = self.valuation.get_bundle_value(frozenset(), self.base_values)
        self.assertEqual(value, 0.0)

    def test_single_item_bundle(self):
        value = self.valuation.get_bundle_value(frozenset({1}), self.base_values)
        self.assertEqual(value, 20.0)

    def test_two_item_bundle(self):
        value = self.valuation.get_bundle_value(frozenset({0, 2}), self.base_values)
        self.assertEqual(value, 40.0)  # 10 + 30

    def test_full_bundle(self):
        value = self.valuation.get_bundle_value(frozenset({0, 1, 2, 3}), self.base_values)
        self.assertEqual(value, 100.0)  # 10 + 20 + 30 + 40

    def test_missing_item_treated_as_zero(self):
        value = self.valuation.get_bundle_value(frozenset({0, 99}), self.base_values)
        self.assertEqual(value, 10.0)  # 10 + 0


class TestSynergyValuation(unittest.TestCase):
    def setUp(self):
        self.synergies = {
            frozenset({0, 1}): 5.0,
            frozenset({2, 3}): 15.0,
        }
        self.valuation = SynergyValuation(self.synergies)
        self.base_values = {0: 10.0, 1: 20.0, 2: 30.0, 3: 40.0}

    def test_empty_bundle(self):
        value = self.valuation.get_bundle_value(frozenset(), self.base_values)
        self.assertEqual(value, 0.0)

    def test_single_item_no_synergy(self):
        value = self.valuation.get_bundle_value(frozenset({0}), self.base_values)
        self.assertEqual(value, 10.0)

    def test_pair_with_synergy(self):
        value = self.valuation.get_bundle_value(frozenset({0, 1}), self.base_values)
        self.assertEqual(value, 35.0)  # 10 + 20 + 5

    def test_pair_without_synergy(self):
        value = self.valuation.get_bundle_value(frozenset({0, 2}), self.base_values)
        self.assertEqual(value, 40.0)  # 10 + 30, no synergy

    def test_bundle_with_multiple_synergies(self):
        value = self.valuation.get_bundle_value(frozenset({0, 1, 2, 3}), self.base_values)
        self.assertEqual(value, 120.0)  # 10 + 20 + 30 + 40 + 5 + 15

    def test_partial_synergy_pair_in_bundle(self):
        # Only item 0 from the {0,1} synergy pair
        value = self.valuation.get_bundle_value(frozenset({0, 2, 3}), self.base_values)
        self.assertEqual(value, 95.0)  # 10 + 30 + 40 + 15 (only {2,3} synergy)

    def test_invalid_non_pairwise_synergy(self):
        with self.assertRaises(ValueError):
            SynergyValuation({frozenset({0, 1, 2}): 10.0})

    def test_invalid_negative_synergy(self):
        with self.assertRaises(ValueError):
            SynergyValuation({frozenset({0, 1}): -5.0})

    def test_empty_synergies(self):
        valuation = SynergyValuation({})
        value = valuation.get_bundle_value(frozenset({0, 1}), self.base_values)
        self.assertEqual(value, 30.0)  # Same as additive


class TestSubstitutesValuation(unittest.TestCase):
    def setUp(self):
        self.substitute_groups = [
            frozenset({0, 1}),  # Items 0 and 1 are substitutes
            frozenset({2, 3}),  # Items 2 and 3 are substitutes
        ]
        self.valuation = SubstitutesValuation(self.substitute_groups)
        self.base_values = {0: 10.0, 1: 20.0, 2: 30.0, 3: 40.0, 4: 50.0}

    def test_empty_bundle(self):
        value = self.valuation.get_bundle_value(frozenset(), self.base_values)
        self.assertEqual(value, 0.0)

    def test_single_item_in_substitute_group(self):
        value = self.valuation.get_bundle_value(frozenset({0}), self.base_values)
        self.assertEqual(value, 10.0)

    def test_both_substitutes_takes_max(self):
        value = self.valuation.get_bundle_value(frozenset({0, 1}), self.base_values)
        self.assertEqual(value, 20.0)  # max(10, 20)

    def test_item_not_in_substitute_group(self):
        value = self.valuation.get_bundle_value(frozenset({4}), self.base_values)
        self.assertEqual(value, 50.0)

    def test_mixed_bundle(self):
        # Items 0,1 are substitutes (max=20), item 4 is independent (50)
        value = self.valuation.get_bundle_value(frozenset({0, 1, 4}), self.base_values)
        self.assertEqual(value, 70.0)  # max(10,20) + 50

    def test_multiple_substitute_groups(self):
        # {0,1} -> max=20, {2,3} -> max=40
        value = self.valuation.get_bundle_value(frozenset({0, 1, 2, 3}), self.base_values)
        self.assertEqual(value, 60.0)  # max(10,20) + max(30,40)

    def test_full_bundle_with_independent_item(self):
        value = self.valuation.get_bundle_value(frozenset({0, 1, 2, 3, 4}), self.base_values)
        self.assertEqual(value, 110.0)  # max(10,20) + max(30,40) + 50

    def test_empty_substitute_groups(self):
        valuation = SubstitutesValuation([])
        value = valuation.get_bundle_value(frozenset({0, 1}), self.base_values)
        self.assertEqual(value, 30.0)  # Same as additive


if __name__ == "__main__":
    unittest.main()
