import hashlib, random, urlparse, os, functools

from django import template
from django.conf import settings
register = template.Library()

class FileHashCache(object):
    def __init__(self):
        self.cache = {}
        
    def __call__(self, path, hash_generator):
        if path in self.cache:
            return self.cache[path]
        else:
            file_hash = hash_generator(path)
            self.cache[path] = file_hash
            return file_hash
    
sha1_cache = FileHashCache()

class AssetUrl(object):
    def __init__(self, settings = None):
        self.settings = settings
        
    def process_url(self, url):
        """Process url and return a suitable URL for the app's environment"""
        if hasattr(self.settings, 'APP_DEPLOYMENT_ENV') and self.settings.APP_DEPLOYMENT_ENV != 'local':
            sha1 = self.generate_sha1(self.file_path_from_url(url))
            return self.compose_url(url, sha1)
        else:
            return url
        
    def file_path_from_url(self, url):
        if hasattr(self.settings, 'MEDIA_URL'):
            stripped_url = url.lstrip('/')
            media_url = '%s/' % self.settings.MEDIA_URL.lstrip('/').rstrip('/')
            if stripped_url.find(media_url) == 0:
                url = stripped_url[len(media_url) - 1:]
        return os.path.normpath(os.path.join(self.settings.MEDIA_ROOT, url.lstrip('/')))
    
    def generate_sha1(self, file_path):
        """Generates and return sha1 for the file at file_path"""
        # import hashlib
        hash_func = hashlib.sha1()
        with open(file_path) as f:
            hash_func.update(f.read())
            
        return hash_func.hexdigest()
        
    def compose_url(self, path, sha1):
        """Stitch path and hash together into a CDN url"""
        # import random, os
        host = random.choice(self.settings.CDN_HOSTS)
        uri_path = path + '/' + sha1[0:8] + os.path.splitext(path)[1]
        return urlparse.urlunparse(('http', host, uri_path, '', '', ''))
            
    def fetch_sha1(self, path, sha1_generator):
        """Generate, or return cached, SHA1 for the file at path"""
        return sha1_cache(path, sha1_generator)

asset_url_processor = AssetUrl(settings)

@register.simple_tag
def asset_url(url):
    return asset_url_processor.process_url(url)
