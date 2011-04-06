from django import template
from django.conf import settings

register = template.Library()

@register.tag
def asset_url(parser, token):
    return AssetUrl(token)

class AssetUrl(template.Node):
    def __init__(self, path):
        self.asset_path = path
        
    def render(self, context):
        return "TEMPLATE TAG OUTPUT"
