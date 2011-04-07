# import hashlib, random, urlparse, os, functools
# 
# class memoized(object):
#    """Decorator that caches a function's return value each time it is called.
#    If called later with the same arguments, the cached value is returned, and
#    not re-evaluated.
#    """
#    def __init__(self, func):
#       self.func = func
#       self.cache = {}
#    def __call__(self, *args):
#       try:
#          return self.cache[args]
#       except KeyError:
#          value = self.func(*args)
#          self.cache[args] = value
#          return value
#       except TypeError:
#          # uncachable -- for instance, passing a list as an argument.
#          # Better to not cache than to blow up entirely.
#          return self.func(*args)
#    def __repr__(self):
#       """Return the function's docstring."""
#       return self.func.__doc__
#    def __get__(self, obj, objtype):
#       """Support instance methods."""
#       return functools.partial(self.__call__, obj)
# 
# class FileHashCache(object):
#     def __init__(self):
#         self.cache = {}
#         
#     def __call__(self, path, hash_generator):
#         if path in self.cache:
#             return self.cache[path]
#         else:
#             file_hash = hash_generator(path)
#             self.cache[path] = file_hash
#             return file_hash
#     
# sha1_cache = FileHashCache()
# 
# class AssetUrl(object):
#     def __init__(self, settings = None):
#         self.settings = settings
#         
#     def process_url(self, url):
#         """Process url and return a suitable URL for the app's environment"""
#         if hasattr(self.settings, 'APP_DEPLOYMENT_ENV') and self.settings.APP_DEPLOYMENT_ENV != 'local':
#             sha1 = self.generate_sha1(self.file_path_from_url(url))
#             return self.compose_url(url, sha1)
#         else:
#             return url
#         
#     def file_path_from_url(self, url):                                
#         return os.path.normpath(os.path.join(self.settings.MEDIA_ROOT, url.lstrip('/')))
#     
#     def generate_sha1(self, file_path):
#         """Generates and return sha1 for the file at file_path"""
#         hash_func = hashlib.sha1()
#         with open(file_path) as f:
#             hash_func.update(f.read())
#             
#         return hash_func.hexdigest()
#         
#     def compose_url(self, path, sha1):
#         """Stitch path and hash together into a CDN url"""
#         host = random.choice(self.settings.CDN_HOSTS)
#         uri_path = path + '/' + sha1[0:8] + os.path.splitext(path)[1]
#         return urlparse.urlunparse(('http', host, uri_path, '', '', ''))
#             
#     def fetch_sha1(self, path, sha1_generator):
#         """Generate, or return cached, SHA1 for the file at path"""
#         return sha1_cache(path, sha1_generator)
#         