import importlib.util, json, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("r2r", ROOT / "scripts" / "registry_to_reladraw.py")
M = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(M)
REG = json.loads((ROOT / "experiments" / "EXPERIMENT_REGISTRY.json").read_text(encoding="utf-8"))

class RegistryToReladrawTests(unittest.TestCase):
    def test_every_experiment_rendered(self):
        out = M.build(REG)
        for e in REG["experiments"]:
            self.assertIn(M.esc(e["experiment_id"]), out)

    def test_committed_diagram_is_fresh(self):
        committed = (ROOT / "experiments/exp-19-shirman-trend-intake/cp02/portfolio.reladraw").read_text(encoding="utf-8")
        self.assertEqual(M.build(REG), committed, "rerun scripts/registry_to_reladraw.py --out ...")

    def test_inferred_dependency(self):
        self.assertIn(("EXP-STAGE3-SYNTHETIC", "EXP-12"), M.inferred_dependencies(REG["experiments"]))

if __name__ == "__main__":
    unittest.main()
