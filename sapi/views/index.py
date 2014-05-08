import logging

import web.webapi

from sapi.views import ViewBase


class IndexView(ViewBase):
    def GET(self):
        raise web.webapi.HTTPError('403 Forbidden')

