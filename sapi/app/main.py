import web

import sapi.config.server
import sapi.config.urls

web.config.debug = sapi.config.server.IS_DEBUG

app = web.application(sapi.config.urls.URLS, locals())
