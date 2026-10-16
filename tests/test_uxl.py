"""Tests for uxl.py. Run: python3 -m unittest discover -s tests"""
import contextlib
import io
import os
import sys
import tempfile
import unittest
from types import SimpleNamespace

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "plugins", "ux-lifecycle", "skills", "ux-lifecycle", "scripts"))
import uxl  # noqa: E402


def run(fn, **kw):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn(SimpleNamespace(**kw))
    return buf.getvalue()


class Docs(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False)
        self.tmp.write("---\nname: x\n---\nIntro text\n\n# Title\n## Alpha\nalpha body\n```\n# not a heading\n```\n"
                       "### Alpha detail\ndetail\n## Beta\nbeta body\n")
        self.tmp.close()

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_toc_lists_headings_outside_fences(self):
        text = run(uxl.cmd_toc, doc=self.tmp.name, depth=3)
        self.assertIn("Alpha  L7-", text)
        self.assertIn("Beta  L", text)
        self.assertNotIn("not a heading", text)

    def test_section_stops_at_sibling_heading(self):
        text = run(uxl.cmd_section, doc=self.tmp.name, heading=["alpha"], outline=False, max_matches=1)
        self.assertIn("detail", text)
        self.assertNotIn("beta body", text)

    def test_preamble_skips_front_matter(self):
        text = run(uxl.cmd_section, doc=self.tmp.name, heading=["preamble"], outline=False, max_matches=1)
        self.assertEqual(text.strip(), "Intro text")

    def test_every_specialist_has_a_toc(self):
        for name in sorted(os.listdir(uxl.SPECIALISTS)):
            if os.path.isdir(os.path.join(uxl.SPECIALISTS, name)):
                self.assertIn("tokens", run(uxl.cmd_toc, doc=name, depth=2), name)


class Lint(unittest.TestCase):
    def rules(self, html):
        return {r for r, _ in uxl.lint_text(html)}

    def test_flags_common_problems(self):
        html = ('<html><img src="a.png"><button><svg></svg></button>'
                '<div @click="go()">x</div><input type="text" placeholder="Search">'
                '<a href="#">click here</a><meta name="viewport" content="user-scalable=no">')
        self.assertTrue({"img-alt", "button-name", "click-div", "input-label", "link-href",
                         "vague-link", "html-lang", "zoom-blocked"} <= self.rules(html))

    def test_accepts_accessible_markup(self):
        html = ('<html lang="en"><img src="a.png" alt=""><button aria-label="Close"><svg></svg></button>'
                '<label for="q">Search</label><input id="q" type="text">'
                '<label>Name <input type="text"></label><input type="hidden" name="t">'
                '<a href="/help">Help centre</a><button class="outline-none focus-visible:ring-2">Go</button>')
        self.assertEqual(self.rules(html), set())


class Contrast(unittest.TestCase):
    def test_black_on_white_is_21(self):
        self.assertIn("21.00:1", run(uxl.cmd_contrast, colours=["000", "#ffffff"]))

    def test_light_grey_fails_aa(self):
        self.assertIn("text AA FAIL", run(uxl.cmd_contrast, colours=["9CA3AF", "FFFFFF"]))


class Scan(unittest.TestCase):
    def test_finds_status_choices_and_commented_notifications(self):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "models.py"), "w") as fh:
                fh.write("class Order:\n    STATUS_CHOICES = [\n        ('DRAFT', 'Draft'),\n"
                         "        ('PAID', 'Paid'),\n    ]\n    status__in = ['X', 'Y']\n"
                         "def notify():\n    # send_mail('a')\n    send_mail('b')\n")
            with open(os.path.join(d, "statuses.ts"), "w") as fh:
                fh.write("export type OrderStatus = 'open' | 'closed'\n")
            text = run(uxl.cmd_scan, root=d, limit=10)
        self.assertIn("STATUS_CHOICES: DRAFT, PAID", text)
        self.assertNotIn("status__in", text)
        self.assertIn("OrderStatus: open, closed", text)
        self.assertIn("2 call sites; 1 commented out", text)


class New(unittest.TestCase):
    def test_creates_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            cwd = os.getcwd()
            os.chdir(d)
            try:
                run(uxl.cmd_new, template="feature-brief", name="quick-apply", dest=None, force=False)
                with open("docs/ux/features/quick-apply/brief.md") as fh:
                    self.assertTrue(fh.readline().startswith("# Feature brief: quick apply"))
                with self.assertRaises(SystemExit):
                    run(uxl.cmd_new, template="feature-brief", name="quick-apply", dest=None, force=False)
            finally:
                os.chdir(cwd)


if __name__ == "__main__":
    unittest.main()
