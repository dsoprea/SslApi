import sapi.app.api

URLS = (
    '/api', sapi.app.api.app,
    '/', 'sapi.views.index.IndexView',
)
