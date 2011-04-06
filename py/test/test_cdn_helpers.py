import unittest
import cdn_helpers

class TestAssetUrl(unittest.TestCase):
    def setUp(self):
        self.asset_url = cdn_helpers.AssetUrl()
        
    def test_local_development_passes_through(self):
        self.assertEqual(self.asset_url.process_url('/a/url'), '/a/url')

if __name__ == '__main__':
    unittest.main()
