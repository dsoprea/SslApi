import json

import web

import sapi.config.server
import sapi.config.api.urls

web.config.debug = sapi.config.server.IS_DEBUG

app = web.application(
            sapi.config.api.urls.URLS, 
            globals(), 
            autoreload=sapi.config.server.IS_DEBUG)

def api_wrapper(handler):
    result = handler()
    encoded = json.dumps(result)
    return (encoded + "\n") \
            if sapi.config.server.IS_DEBUG \
            else encoded

app.add_processor(api_wrapper)
