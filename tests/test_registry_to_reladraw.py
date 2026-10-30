import importlib.util, json, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("r2r", ROOT / "scripts" / "registry_to_reladraw.py")
M = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(M)
REG = json.loads((ROOT / "experiments" / "EXPERIMENT_REGISTRY.json").read_text(encoding="utf-8"))

class DisplayLayoutTests(unittest.TestCase):
    def test_short_preserves_long_tokens_and_spaced_slashes(self):
        token = "docs/experiments/EXP-13_CLOUDFLARE_RELAY_PREFLIGHT.md"
        self.assertEqual(M.short(token, 70), token)
        self.assertEqual(M.short("Strix / FreeBuff", 40), "Strix / FreeBuff")

    def test_long_token_svg_lines_keep_one_copyable_text_content(self):
        import xml.etree.ElementTree as ET
        token = "docs/experiments/EXP-13_CLOUDFLARE_RELAY_PREFLIGHT.md"
        source = M.build_status_view({"experiments": [{
            "experiment_id": "EXP-13", "owning_project": "Murat Project Engineer",
            "name": "Low-cost evaluation harness", "status": "READY_TO_TEST",
            "next_action": "Run " + token + ".",
        }], "updated_at": "2026-10-29"}, "READY_TO_TEST")
        self.assertIn(M.CONTINUATION, source)
        # The committed render is produced by the pinned renderer + documented
        # SVG post-pass; its textContent must not contain inserted spaces.
        svg = (MOBILE / "status-ready_to_test.svg").read_text(encoding="utf-8")
        root = ET.fromstring(svg)
        texts = ["".join(e.itertext()) for e in root.iter() if e.tag.endswith("text")]
        self.assertTrue(any(token in text for text in texts), texts)
        joined = ET.fromstring(M.join_svg_continuations(svg))
        self.assertEqual(
            ["".join(e.itertext()) for e in joined.iter() if e.tag.endswith("text")],
            texts,
        )
        spans = [e for e in root.iter() if e.tag.endswith("tspan")]
        self.assertGreater(len(spans), 1)
        self.assertTrue(all("x" in e.attrib and "y" in e.attrib for e in spans))
        # Prove the post-pass on raw renderer-shaped output, not only on the
        # already-joined committed artifact. The two visual lines must become
        # one copyable text node, and a second pass must be a no-op.
        raw = (
            '<svg xmlns="http://www.w3.org/2000/svg">'
            '<text x="10" y="20">docs/experiments/EXP-13_CL</text>'
            f'<text x="10" y="39">{M.CONTINUATION}OUDFLARE_RELAY_PREFLIGHT.md</text>'
            '<text x="10" y="58">unrelated</text></svg>'
        )
        joined_raw = M.join_svg_continuations(raw)
        raw_root = ET.fromstring(joined_raw)
        raw_texts = ["".join(e.itertext()) for e in raw_root.iter() if e.tag.endswith("text")]
        self.assertEqual(raw_texts, [token, "unrelated"])
        self.assertEqual(M.join_svg_continuations(joined_raw), joined_raw)


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
