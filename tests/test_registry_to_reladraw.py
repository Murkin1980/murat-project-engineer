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


MOBILE = ROOT / "experiments/exp-19-shirman-trend-intake/cp02/mobile"


class MobileViewTests(unittest.TestCase):
    def test_each_experiment_in_exactly_one_status_view(self):
        seen = []
        for st in {e["status"] for e in REG["experiments"]}:
            out = M.build_status_view(REG, st)
            seen += [e["experiment_id"] for e in REG["experiments"] if f'col.{M.slug(e["experiment_id"])} ' in out]
        self.assertEqual(sorted(seen), sorted(e["experiment_id"] for e in REG["experiments"]))

    def test_committed_mobile_views_are_fresh(self):
        for st in {e["status"] for e in REG["experiments"]}:
            path = MOBILE / f"status-{M.slug(st)}.reladraw"
            self.assertEqual(M.build_status_view(REG, st), path.read_text(encoding="utf-8"), path.name)

    def test_rendered_mobile_svgs_fit_390px_unscaled(self):
        import re
        svgs = sorted(MOBILE.glob("status-*.svg"))
        self.assertTrue(svgs)
        for svg in svgs:
            head = svg.read_text(encoding="utf-8")[:400]
            width = int(re.search(r'width="(\d+)"', head).group(1))
            self.assertLessEqual(width, 390, svg.name)
            self.assertIn('font-size="14px"', head)

    def test_no_depends_on_in_registry(self):
        self.assertFalse(any("depends_on" in e for e in REG["experiments"]))
