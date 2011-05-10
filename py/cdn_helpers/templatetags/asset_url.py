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
            sha1 = self.fetch_sha1(self.file_path_from_url(url), self.generate_sha1)
            if sha1 != None:
                url = self.compose_path(url, sha1)
            return self.compose_url(url)
        else:
            return url
        
    def file_path_from_url(self, url):
        if hasattr(self.settings, 'MEDIA_URL'):
            stripped_url = url.lstrip('/')
            media_url = '%s/' % self.settings.MEDIA_URL.lstrip('/').rstrip('/')
            if stripped_url.find(media_url) == 0:
                url = stripped_url[len(media_url) - 1:]
        local_path = os.path.normpath(os.path.join(self.settings.MEDIA_ROOT, url.lstrip('/')))
        if os.path.exists(local_path):
            return local_path
        if hasattr(self.settings, 'SHARED_PUBLIC_ROOT'):
            shared_path = os.path.normpath(os.path.join(self.settings.SHARED_PUBLIC_ROOT, url.lstrip('/')))
            if os.path.exists(shared_path):
                return shared_path
        return None
    
    def generate_sha1(self, file_path):
        """Generates and return sha1 for the file at file_path"""
        # import hashlib
        if file_path == None:
            return None
        hash_func = hashlib.sha1()
        with open(file_path) as f:
            hash_func.update(f.read())
            
        return hash_func.hexdigest()

    def compose_path(self, path, sha1):
        """Stitch path and hash together"""
        return path + '/' + sha1[0:8] + self.hash_salt() + os.path.splitext(path)[1]
        
    def compose_url(self, uri_path):
        """Stitch hashed path into a CDN url"""
        # import random, os
        host = random.choice(self.settings.CDN_HOSTS)
        return urlparse.urlunparse(('http', host, uri_path, '', '', ''))
            
    def fetch_sha1(self, path, sha1_generator):
        """Generate, or return cached, SHA1 for the file at path"""
        return sha1_cache(path, sha1_generator)
    
    def hash_salt(self):
        if hasattr(self.settings, 'CDN_HASH_SALT'):
            return self.settings.CDN_HASH_SALT
        return 'X'

asset_url_processor = AssetUrl(settings)

@register.simple_tag
def asset_url(url):
    return asset_url_processor.process_url(url)
