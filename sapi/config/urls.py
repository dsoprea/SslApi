import sapi.app.api

URLS = (
    '/api', sapi.app.api.app,

    '/ping', 'sapi.views.ping.PingView',
    '/', 'sapi.views.index.IndexView',
)
