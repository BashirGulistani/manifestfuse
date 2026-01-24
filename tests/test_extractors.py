import unittest
from manifestfuse.extractors import extract_refs_from_text



class TestExtractors(unittest.TestCase):
    def test_liquid_asset_url(self):
        t = """{{ 'main.css' | asset_url | stylesheet_tag }}"""
        refs = extract_refs_from_text(t)
        self.assertIn("main.css", refs)

