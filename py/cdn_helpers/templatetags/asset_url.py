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

@register.tag
def asset_url(parser, token):
    tag_name, url_or_lookup = token.split_contents()
    url = None
    lookup = None
    if url_or_lookup.startswith(("'", '"')):
        url = url_or_lookup[1:-1]
    else:
        lookup = url_or_lookup
        
    return AssetUrlTag(url = url, lookup = lookup)

class AssetUrlTag(template.Node):
    def __init__(self, url = None, lookup = None):
        self.asset_url = url
        if lookup != None:
            self.asset_lookup = template.Variable(lookup)
        self.url_gen = AssetUrl(settings)
        
    def render(self, context):
        if self.asset_url != None:
            url_to_process = self.asset_url
        else:
            url_to_process = self.asset_lookup.resolve(context)
        return self.url_gen.process_url(self.asset_url)
