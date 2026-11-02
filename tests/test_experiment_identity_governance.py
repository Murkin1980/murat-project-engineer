"""Regression checks for the canonical experiment identity gate.

These checks validate only persisted registry invariants. FIFO ordering and
semantic deduplication require the mandatory pre-registration review recorded
in the governance standard; they cannot be inferred from a JSON snapshot.
"""

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "experiments" / "EXPERIMENT_REGISTRY.json"
STANDARD = ROOT / "docs" / "governance" / "EXPERIMENT_IDENTITY_NAMING_STANDARD_PROPOSAL.md"


class ExperimentIdentityGovernanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.experiments = json.loads(REGISTRY.read_text(encoding="utf-8"))["experiments"]

    def test_canonical_ids_and_titles_are_unique(self):
        ids = [entry["experiment_id"] for entry in self.experiments]
        names = [entry["name"].strip().casefold() for entry in self.experiments]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(names), len(set(names)))

    def test_retired_exp_34_cannot_be_registered(self):
        self.assertNotIn("EXP-34", {entry["experiment_id"] for entry in self.experiments})

    def test_fifo_allocation_and_historical_ids_are_preserved(self):
        ids = {entry["experiment_id"] for entry in self.experiments}
        expected_fifo = {f"EXP-{number:02d}" for number in range(30, 47)} - {"EXP-34"}
        self.assertTrue(expected_fifo.issubset(ids))
        self.assertTrue({"EXP-ALEXANDRIA", "EXP-RANKCONTROL", "EXP-002"}.issubset(ids))

    def test_standard_requires_all_agent_interfaces_and_gate_order(self):
        text = STANDARD.read_text(encoding="utf-8")
        for token in ("ChatGPT", "Work", "Arena", "Codex", "GitHub", "UNNUMBERED / DRAFT"):
            self.assertIn(token, text)
        for marker in ("A.", "B.", "C.", "D.", "E.", "F.", "G."):
            self.assertIn(marker, text)
        self.assertRegex(text, re.compile(r"EXP-34.*never reused", re.DOTALL))


if __name__ == "__main__":
    unittest.main()
