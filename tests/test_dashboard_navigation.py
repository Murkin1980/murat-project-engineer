from html.parser import HTMLParser
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "dashboard" / "public" / "index.html"
EXPECTED_TARGETS = {"brief", "p0", "support", "hold", "decisions"}


class DashboardParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.jump_targets = set()
        self.in_jump_nav = False

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"])
        if tag == "nav" and "jump-nav" in values.get("class", "").split():
            self.in_jump_nav = True
        if self.in_jump_nav and tag == "a" and values.get("href", "").startswith("#"):
            self.jump_targets.add(values["href"][1:])

    def handle_endtag(self, tag):
        if tag == "nav" and self.in_jump_nav:
            self.in_jump_nav = False


class DashboardNavigationTests(unittest.TestCase):
    def test_navigation_targets_existing_sections(self):
        parser = DashboardParser()
        parser.feed(DASHBOARD.read_text(encoding="utf-8"))

        self.assertEqual(parser.jump_targets, EXPECTED_TARGETS)
        self.assertTrue(EXPECTED_TARGETS.issubset(parser.ids))


if __name__ == "__main__":
    unittest.main()
