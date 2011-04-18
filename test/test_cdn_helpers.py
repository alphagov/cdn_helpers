import unittest
import cdn_helpers.templatetags.asset_url as cdn_helpers
import os

fixtures_dir = os.path.join(os.path.dirname(__file__), '..', 'fixtures')

class MockSettings(object):
    def __init__(self):
        self.settings = {}
        
    def __setitem__(self, name, value):
        object.__getattribute__(self, 'settings')[name] = value
        
    def __getattribute__(self, name):
        return object.__getattribute__(self, 'settings')[name]

class TestAssetUrlLocal(unittest.TestCase):
    def setUp(self):
        self.django_settings = MockSettings()
        self.asset_url = cdn_helpers.AssetUrl(self.django_settings)
        
    def test_local_development_passes_through(self):
        self.django_settings['APP_DEPLOYMENT_ENV'] = 'local'
        self.assertEqual(self.asset_url.process_url('/a/url'), '/a/url')

class TestAssetUrlModification(unittest.TestCase):
    def setUp(self):
        self.django_settings = MockSettings()
        self.asset_url = cdn_helpers.AssetUrl(self.django_settings)
        
    def test_sha1_calculation(self):
        self.assertEqual(
            self.asset_url.generate_sha1(os.path.join(fixtures_dir, 'h5.png')), 
            'daf4a94f8d2cc9f564a6f958d1915ea9346d09f1'
        )

    def test_sha1_calculation_returns_None_if_passed_None(self):
        self.assertEqual(
            self.asset_url.generate_sha1(None), 
            None
        )
        
    def test_url_generation(self):
        self.django_settings['CDN_HOSTS'] = ['dev1.host.com']
        
        self.assertEqual(
            self.asset_url.compose_url('/images/h5.png/daf4a94f.png'),
            'http://dev1.host.com/images/h5.png/daf4a94f.png'
        )

class TestAssetSha1Caching(unittest.TestCase):
    def setUp(self):
        self.asset_url = cdn_helpers.AssetUrl()
        
    def test_sha1_caching(self):
        def mock_sha1_generator(path):
            mock_sha1_generator.count += 1
            if mock_sha1_generator.count > 1: 
                raise AssertionError()
            return 'sha1value'
        mock_sha1_generator.count = 0
        
        self.assertEqual(
            self.asset_url.fetch_sha1('/images/h5.png', mock_sha1_generator),
            'sha1value'
        )
        self.assertEqual(
            self.asset_url.fetch_sha1('/images/h5.png', mock_sha1_generator),
            'sha1value'
        )

class TestAssetFileLocation(unittest.TestCase):
    def setUp(self):
        self.django_settings = MockSettings()
        self.asset_url = cdn_helpers.AssetUrl(self.django_settings)
        
    def test_correctly_locates_a_file(self):
        self.django_settings['MEDIA_ROOT'] = fixtures_dir
        
        self.assertEqual(
            self.asset_url.file_path_from_url('/images/thing.png'), 
            os.path.normpath(os.path.join(fixtures_dir, 'images/thing.png'))
        )

    def test_correctly_locates_a_file_when_media_url_is_set(self):
        self.django_settings['MEDIA_ROOT'] = fixtures_dir
        self.django_settings['MEDIA_URL'] = '/media_url/'

        self.assertEqual(
            self.asset_url.file_path_from_url('/media_url/images/thing.png'), 
            os.path.normpath(os.path.join(fixtures_dir, 'images/thing.png'))
        )

    def test_correctly_locates_a_shared_file_if_SHARED_PUBLIC_ROOT_is_set(self):
        self.django_settings['MEDIA_ROOT'] = fixtures_dir
        self.django_settings['MEDIA_URL'] = '/media_url/'
        self.django_settings['SHARED_PUBLIC_ROOT'] = os.path.join(fixtures_dir, 'files_from_static')

        self.assertEqual(
            self.asset_url.file_path_from_url('/media_url/images/answers-advisory-highlight.png'), 
            os.path.normpath(os.path.join(fixtures_dir, 'files_from_static', 'images/answers-advisory-highlight.png'))
        )

    def test_returns_None_for_a_shared_file_if_SHARED_PUBLIC_ROOT_is_not_set(self):
        self.django_settings['MEDIA_ROOT'] = fixtures_dir
        self.django_settings['MEDIA_URL'] = '/media_url/'

        self.assertEqual(
            self.asset_url.file_path_from_url('/media_url/images/answers-advisory-highlight.png'), 
            None
        )

    def test_returns_None_if_file_cannot_be_located(self):
        self.django_settings['MEDIA_ROOT'] = fixtures_dir
        self.django_settings['MEDIA_URL'] = '/media_url/'

        self.assertEqual(
            self.asset_url.file_path_from_url('/media_url/unreal.css'), 
            None
        )

class TestAssetUrlFromCDN(unittest.TestCase):
    def setUp(self):
        self.django_settings = MockSettings()
        self.asset_url = cdn_helpers.AssetUrl(self.django_settings)
        
    def test_cdn_url_created(self):
        self.django_settings['MEDIA_ROOT'] = fixtures_dir
        self.django_settings['APP_DEPLOYMENT_ENV'] = 'dev'
        self.django_settings['CDN_HOSTS'] = ['cdn.host.com']
        self.assertEqual(self.asset_url.process_url('/h5.png'), 'http://cdn.host.com/h5.png/daf4a94f.png')

    def test_cdn_url_returns_unhashed_url_if_file_not_found(self):
        self.django_settings['MEDIA_ROOT'] = fixtures_dir
        self.django_settings['APP_DEPLOYMENT_ENV'] = 'dev'
        self.django_settings['CDN_HOSTS'] = ['cdn.host.com']
        self.assertEqual(self.asset_url.process_url('/h51.png'), 'http://cdn.host.com/h51.png')


if __name__ == '__main__':
    unittest.main()
