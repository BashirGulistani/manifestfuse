import unittest
from manifestfuse.extractors import extract_refs_from_text



class TestExtractors(unittest.TestCase):
    def test_liquid_asset_url(self):
        t = """{{ 'main.css' | asset_url | stylesheet_tag }}"""
        refs = extract_refs_from_text(t)
        self.assertIn("main.css", refs)

    def test_css_url(self):
        t = """.x{ background:url('/assets/a.png?v=1'); }"""
        refs = extract_refs_from_text(t)
        self.assertIn("/assets/a.png", refs)

    def test_srcset(self):
        t = """<img srcset="a.png 1x, b.png 2x" />"""
        refs = extract_refs_from_text(t)
        self.assertIn("a.png", refs)
        self.assertIn("b.png", refs)


if __name__ == "__main__":
    unittest.main()
