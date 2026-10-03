"""Guard: HyperFrames compositions render offline.

Every HyperFrames `index.html` (prototypes and any beat under `videos/`)
must load scripts, stylesheets and fonts from local files, and the vendored
files must match the sha256 recorded in `videos/_shared/web/vendor/README.md`.
No network, no rendering.
"""
from __future__ import annotations

import hashlib
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
VENDOR = REPO / "videos" / "_shared" / "web" / "vendor"
SKIP_DIRS = {"node_modules", "media", "out", "renders", "_graveyard"}

# A remote load is a URL with a scheme (or protocol-relative //) in a
# <script src>, <link href>, CSS url(...) or @import. Plain text, comments
# and the SVG xmlns attribute are not loads.
REMOTE = [
    re.compile(r"<script\b[^>]*\bsrc\s*=\s*[\"']?\s*(https?:)?//", re.I),
    re.compile(r"<link\b[^>]*\bhref\s*=\s*[\"']?\s*(https?:)?//", re.I),
    re.compile(r"url\(\s*[\"']?\s*(https?:)?//", re.I),
    re.compile(r"@import\s+[\"']?\s*(url\()?\s*[\"']?\s*(https?:)?//", re.I),
]
ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|.*\|\s*`([0-9a-f]{64})`\s*\|\s*$")


def compositions() -> list[Path]:
    roots = [REPO / "prototypes" / "hyperframes", REPO / "videos"]
    found = []
    for root in roots:
        for path in root.rglob("index.html"):
            if SKIP_DIRS.intersection(path.relative_to(REPO).parts):
                continue
            if path.is_relative_to(VENDOR):
                continue
            found.append(path)
    return sorted(found)


def vendored() -> dict[str, str]:
    rows = {}
    for line in (VENDOR / "README.md").read_text().splitlines():
        m = ROW.match(line)
        if m:
            rows[m.group(1)] = m.group(2)
    return rows


class TestRemotePatterns(unittest.TestCase):
    def test_patterns_catch_remote_loads(self):
        bad = [
            '<script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>',
            "<script src='//cdn.example.com/x.js'></script>",
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter">',
            "src: url(https://fonts.gstatic.com/s/inter.woff2)",
            '@import url("https://fonts.googleapis.com/css2?family=Inter");',
        ]
        for text in bad:
            self.assertTrue(any(p.search(text) for p in REMOTE), text)

    def test_patterns_allow_local_loads(self):
        ok = [
            '<script src="vendor/gsap.min.js"></script>',
            'src: url("vendor/Inter-ExtraBold.woff2") format("woff2");',
            '<svg xmlns="http://www.w3.org/2000/svg">',
            "<!-- was https://cdn.jsdelivr.net/npm/gsap -->",
        ]
        for text in ok:
            self.assertFalse(any(p.search(text) for p in REMOTE), text)


class TestCompositionsOffline(unittest.TestCase):
    def test_prototypes_are_found(self):
        names = {p.parent.name for p in compositions()}
        self.assertTrue({"quiz", "ironies"} <= names, names)

    def test_no_remote_loads(self):
        for path in compositions():
            text = path.read_text()
            for pattern in REMOTE:
                m = pattern.search(text)
                self.assertIsNone(
                    m, f"{path.relative_to(REPO)}: remote load {m and m.group(0)!r}"
                )

    def test_vendor_links_resolve_to_shared_vendor(self):
        for path in compositions():
            if "vendor/" not in path.read_text():
                continue
            link = path.parent / "vendor"
            self.assertTrue(link.exists(), f"{link.relative_to(REPO)} missing")
            self.assertEqual(link.resolve(), VENDOR.resolve(), str(link))


class TestVendoredFiles(unittest.TestCase):
    def test_readme_lists_files(self):
        rows = vendored()
        self.assertIn("gsap.min.js", rows)
        self.assertIn("Inter-ExtraBold.woff2", rows)

    def test_files_match_recorded_sha256(self):
        for name, digest in vendored().items():
            path = VENDOR / name
            self.assertTrue(path.is_file(), f"{name} missing")
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(actual, digest, f"{name} sha256 changed")


if __name__ == "__main__":
    unittest.main()
