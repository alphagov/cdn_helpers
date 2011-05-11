from django.core.management.base import BaseCommand
from django.conf import settings
import glob, os.path
from subprocess import call

class Command(BaseCommand):
  def handle(self, *args, **options):
      path_to_ruby_script = os.path.normpath(os.path.join(os.path.dirname(__file__), '../../../../process_css'))
      css_file_paths = glob.glob(os.path.join(settings.MEDIA_ROOT, '**/*.css'))
      
      for css_file_path in css_file_paths:
          args = [path_to_ruby_script, css_file_path, settings.MEDIA_ROOT, settings.MEDIA_URL]
          if hasattr(settings, 'CDN_HASH_SALT'):
              args.append(settings.CDN_HASH_SALT)
          call(args)
      
