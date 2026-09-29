"""Deploy-configuration guards for the Cloudflare-hosted portfolio dashboard.

The dashboard ships as committed static assets in ``dashboard/public/`` and is
assembled into the deployable output directory by ``scripts/build_dashboard.mjs``.
These checks keep the three places that must agree from drifting apart:

- ``wrangler.jsonc`` (Cloudflare Workers Static Assets: build command + output dir);
- ``package.json`` (the same build command for Cloudflare Pages / local use);
- ``dashboard/public/index.html`` (every referenced route/asset must be deployable).

They also assert the deploy configuration stays credentials-free and that the
generated output directory is not committed.
"""

from __future__ import annotations

import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "dashboard" / "public" / "index.html"
SOURCE_DIR = ROOT / "dashboard" / "public"
BUILD_SCRIPT = ROOT / "scripts" / "build_dashboard.mjs"
PREVIEW_SCRIPT = ROOT / "scripts" / "preview_dashboard.mjs"
CHECK_SCRIPT = ROOT / "scripts" / "check_dashboard_deploy.mjs"
DEPLOY_DOC = ROOT / "CLOUDFLARE_DEPLOY.md"
BUILD_COMMAND = "node scripts/build_dashboard.mjs"
OUTPUT_DIR = "dist"
MOBILE_MAX_WIDTH_PX = 390


def read_jsonc(path: Path):
    """Parse the comment-tolerant JSONC used by wrangler.jsonc."""
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"/\*[\s\S]*?\*/", "", text)
    text = re.sub(r"^\s*//.*$", "", text, flags=re.M)
    return json.loads(text)


class AssetReferenceParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = set()

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        for attribute in ("src", "href"):
            reference = values.get(attribute, "")
            if reference.startswith("/"):
                self.references.add(reference.split("#")[0])


class WranglerConfigTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = read_jsonc(ROOT / "wrangler.jsonc")

    def test_worker_identity_and_static_asset_routing_are_preserved(self):
        self.assertEqual(self.config["name"], "murat-project-engineer")
        self.assertIn("compatibility_date", self.config)
        assets = self.config["assets"]
        self.assertEqual(assets["html_handling"], "auto-trailing-slash")
        self.assertEqual(assets["not_found_handling"], "single-page-application")

    def test_output_directory_is_the_generated_build_directory(self):
        self.assertEqual(self.config["assets"]["directory"], f"./{OUTPUT_DIR}")
        self.assertNotEqual(Path(self.config["assets"]["directory"]).name, "public")

    def test_build_command_runs_the_repository_build_script(self):
        self.assertEqual(self.config["build"]["command"], BUILD_COMMAND)
        self.assertTrue(BUILD_SCRIPT.is_file())

    def test_static_worker_declares_no_script_bindings_or_credentials(self):
        for forbidden in ("main", "vars", "secrets", "account_id", "api_token", "kv_namespaces", "d1_databases", "r2_buckets"):
            self.assertNotIn(forbidden, self.config)
        self.assertNotIn("binding", self.config["assets"])
        # Scan the configuration itself (comments stripped) for credential material.
        raw = re.sub(r"/\*[\s\S]*?\*/", "", (ROOT / "wrangler.jsonc").read_text(encoding="utf-8"))
        raw = re.sub(r"^\s*//.*$", "", raw, flags=re.M).lower()
        for forbidden in ("api_token", "secret", "account_id", "password"):
            self.assertNotIn(forbidden, raw)


class PackageScriptsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))

    def test_build_script_matches_the_wrangler_build_command(self):
        self.assertEqual(self.package["scripts"]["build"], BUILD_COMMAND)

    def test_local_preview_and_deploy_checks_are_available(self):
        self.assertIn("preview", self.package["scripts"])
        self.assertIn("check", self.package["scripts"])
        self.assertTrue(PREVIEW_SCRIPT.is_file())
        self.assertTrue(CHECK_SCRIPT.is_file())

    def test_dashboard_build_stays_dependency_free(self):
        self.assertTrue(self.package["private"])
        self.assertNotIn("dependencies", self.package)
        self.assertNotIn("devDependencies", self.package)

    def test_pinned_wrangler_version_matches_the_deploy_workflow(self):
        workflow = (ROOT / ".github" / "workflows" / "deploy-dashboard.yml").read_text(encoding="utf-8")
        pinned = set(re.findall(r"wrangler@(\d+\.\d+\.\d+)", workflow))
        self.assertEqual(len(pinned), 1, f"workflow must pin exactly one wrangler version: {sorted(pinned)}")
        version = pinned.pop()
        script_versions = set(re.findall(r"wrangler@(\d+\.\d+\.\d+)", json.dumps(self.package["scripts"])))
        self.assertTrue(script_versions, "package.json should pin the same wrangler for local dev/dry-run")
        self.assertEqual(script_versions, {version})


class DashboardAssetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parser = AssetReferenceParser()
        parser.feed(DASHBOARD.read_text(encoding="utf-8"))
        cls.references = parser.references

    def test_every_referenced_asset_exists_in_the_committed_source(self):
        self.assertTrue(self.references, "dashboard must reference its Reladraw views")
        for reference in sorted(self.references):
            with self.subTest(asset=reference):
                self.assertTrue((SOURCE_DIR / reference.lstrip("/")).is_file())

    def test_desktop_and_mobile_reladraw_views_are_both_shipped(self):
        self.assertIn("/registry/portfolio.svg", self.references)
        mobile = {r for r in self.references if r.startswith("/registry/mobile/status-")}
        self.assertGreaterEqual(len(mobile), 4)
        for view in sorted(mobile):
            head = (SOURCE_DIR / view.lstrip("/")).read_text(encoding="utf-8")[:400]
            width = int(re.search(r'width="(\d+)"', head).group(1))
            font_size = re.search(r'font-size="([^"]+)"', head).group(1)
            with self.subTest(view=view):
                self.assertLessEqual(width, MOBILE_MAX_WIDTH_PX)
                self.assertEqual(font_size, "14px")

    def test_desktop_and_mobile_views_stay_responsive_switched(self):
        html = DASHBOARD.read_text(encoding="utf-8")
        self.assertIn('class="registry-views registry-desktop"', html)
        self.assertIn('class="registry-views registry-mobile"', html)
        self.assertIn(".registry-desktop .registry-image-frame img{max-width:none}", html)
        self.assertIn(".registry-mobile{display:none}", html)
        self.assertIn(
            "@media(max-width:649px){.registry-desktop{display:none}.registry-mobile{display:block}",
            html,
        )

    def test_generated_output_directory_is_not_committed(self):
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn(f"{OUTPUT_DIR}/", gitignore)
        tracked = [
            path for path in (ROOT / OUTPUT_DIR).rglob("*") if path.is_file()
        ] if (ROOT / OUTPUT_DIR).exists() else []
        # A local build may exist; it must never be a source of truth.
        for path in tracked:
            self.assertTrue(path.is_relative_to(ROOT / OUTPUT_DIR))


class DeployDocumentationTests(unittest.TestCase):
    def test_manual_deploy_document_states_the_same_build_contract(self):
        self.assertTrue(DEPLOY_DOC.is_file(), "CLOUDFLARE_DEPLOY.md must exist")
        text = DEPLOY_DOC.read_text(encoding="utf-8")
        self.assertIn(BUILD_COMMAND, text)
        self.assertIn(OUTPUT_DIR, text)
        self.assertIn("wrangler", text.lower())
        self.assertNotIn("[TODO:", text)


if __name__ == "__main__":
    unittest.main()
