"""Freshness and integration guards for the dashboard's Reladraw views.

The rendered SVGs are deployment copies of the CP-02 artifacts. The existing
registry-to-Reladraw tests ensure the Reladraw sources match the canonical
registry; these checks ensure the dashboard exposes the matching renders.
"""

import importlib.util
import json
import re
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "dashboard" / "public" / "index.html"
PUBLIC_VIEWS = ROOT / "dashboard" / "public" / "registry"
CP02 = ROOT / "experiments" / "exp-19-shirman-trend-intake" / "cp02"
REGISTRY = json.loads(
    (ROOT / "experiments" / "EXPERIMENT_REGISTRY.json").read_text(encoding="utf-8")
)
SPEC = importlib.util.spec_from_file_location(
    "registry_to_reladraw", ROOT / "scripts" / "registry_to_reladraw.py"
)
RELADRAW = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RELADRAW)


class DashboardViewParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.image_sources = set()

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"])
        if tag == "img" and values.get("src"):
            self.image_sources.add(values["src"])


class DashboardRegistryViewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = DASHBOARD.read_text(encoding="utf-8")
        cls.parser = DashboardViewParser()
        cls.parser.feed(cls.html)

    def test_dashboard_exposes_the_generated_desktop_portfolio(self):
        self.assertIn("registry", self.parser.ids)
        self.assertIn("/registry/portfolio.svg", self.parser.image_sources)
        self.assertIn("experiments/EXPERIMENT_REGISTRY.json", self.html)
        self.assertIn("scripts/registry_to_reladraw.py", self.html)

    def test_dashboard_exposes_a_mobile_view_for_each_registry_status(self):
        for status in {e["status"] for e in REGISTRY["experiments"]}:
            asset = f"/registry/mobile/status-{RELADRAW.slug(status)}.svg"
            with self.subTest(status=status):
                self.assertIn(asset, self.parser.image_sources)

    def test_dashboard_renders_match_the_validated_cp02_artifacts(self):
        pairs = [(PUBLIC_VIEWS / "portfolio.svg", CP02 / "portfolio.svg")]
        for status in {e["status"] for e in REGISTRY["experiments"]}:
            name = f"status-{RELADRAW.slug(status)}.svg"
            pairs.append((PUBLIC_VIEWS / "mobile" / name, CP02 / "mobile" / name))

        for dashboard_view, validated_view in pairs:
            with self.subTest(view=dashboard_view.name):
                self.assertTrue(dashboard_view.is_file(), f"missing {dashboard_view}")
                self.assertEqual(dashboard_view.read_bytes(), validated_view.read_bytes())

    def test_rendered_dashboard_text_tracks_registry_ids_names_and_next_steps(self):
        views = [(PUBLIC_VIEWS / "portfolio.svg", REGISTRY["experiments"], 30, 48)]
        for status in {e["status"] for e in REGISTRY["experiments"]}:
            items = [e for e in REGISTRY["experiments"] if e["status"] == status]
            views.append((PUBLIC_VIEWS / "mobile" / f"status-{RELADRAW.slug(status)}.svg", items, 40, 70))

        for path, items, name_chars, next_chars in views:
            svg_root = ET.parse(path).getroot()
            rendered = " ".join(
                " ".join((element.text or "").split())
                for element in svg_root.iter()
                if element.tag.endswith("text")
            )
            with self.subTest(view=path.name):
                for experiment in items:
                    for field, expected in (
                        ("experiment_id", experiment["experiment_id"]),
                        ("name", RELADRAW.short(experiment["name"], name_chars)),
                        (
                            "next_action",
                            "→ " + RELADRAW.short(experiment.get("next_action", ""), next_chars),
                        ),
                    ):
                        with self.subTest(experiment=experiment["experiment_id"], field=field):
                            self.assertIn(" ".join(expected.split()), rendered)

    def test_dashboard_mobile_views_fit_390px_at_native_readable_text_size(self):
        for status in {e["status"] for e in REGISTRY["experiments"]}:
            path = PUBLIC_VIEWS / "mobile" / f"status-{RELADRAW.slug(status)}.svg"
            head = path.read_text(encoding="utf-8")[:400]
            width = int(re.search(r'width="(\d+)"', head).group(1))
            font_size = re.search(r'font-size="([^"]+)"', head).group(1)
            with self.subTest(status=status):
                self.assertLessEqual(width, 390)
                self.assertEqual(font_size, "14px")

        # At 390px, the section has 362px after the app's 14px side padding;
        # the image frame breaks out of the card's inner padding to preserve
        # the SVGs' native 346–355px width and 14px text without zoom.
        self.assertIn("width:min(calc(100vw - 28px),1649px)", self.html)
        self.assertIn("margin:10px -14px", self.html)


if __name__ == "__main__":
    unittest.main()
