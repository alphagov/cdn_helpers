from django import template
from django.conf import settings
import cdn_helpers
register = template.Library()

@register.tag
def asset_url(parser, token):
    tag_name, url_or_lookup = token.split_contents()
    url = None
    lookup = None
    if url_or_lookup.startswith(("'", '"')):
        url = url_or_lookup
    else:
        lookup = url_or_lookup
        
    return AssetUrl(url = url, lookup = lookup)

class AssetUrl(template.Node):
    def __init__(self, url = None, lookup = None):
        self.asset_url = url
        if lookup != None:
            self.asset_lookup = template.Variable(lookup)
        self.url_gen = cdn_helpers.AssetUrl(settings)
        
    def render(self, context):
        if self.asset_url != None:
            url_to_process = self.asset_url
        else:
            url_to_process = self.asset_lookup.resolve(context)
        return self.url_gen.process_url(self.asset_url)
