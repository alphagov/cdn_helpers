from django import template
from django.conf import settings

def asset_url(parser, token):
    return AsetUrl(token)

class AsetUrl(template.Node):
    def __init__(self, path):
        self.asset_path = path
    def render(self, context):
        return "TEMPLATE TAG OUTPUT"
