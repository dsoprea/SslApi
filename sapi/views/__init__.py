from web.contrib.template import render_jinja
from web import ctx

from sapi.config.server import TEMPLATE_PATH, TEMPLATE_GLOBALS


class ViewBase(object):
    def __init__(self, *args, **kwargs):
        self.ctx = ctx
        self.env = ctx.env
        self.render = render_jinja(TEMPLATE_PATH, globals=TEMPLATE_GLOBALS)
