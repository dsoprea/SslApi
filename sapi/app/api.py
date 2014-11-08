import json

import web

import sapi.config.general
import sapi.config.api.urls

_IS_DEBUG = sapi.config.general.IS_DEBUG

web.config.debug = _IS_DEBUG

app = web.application(
            sapi.config.api.urls.URLS, 
            globals(), 
            autoreload=_IS_DEBUG)

def api_wrapper(handler):
    result = handler()
    encoded = json.dumps(result)
    return (encoded + "\n") if _IS_DEBUG else encoded

app.add_processor(api_wrapper)
