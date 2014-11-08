import web

import sapi.config.general
import sapi.config.urls

web.config.debug = sapi.config.general.IS_DEBUG

app = web.application(sapi.config.urls.URLS, locals())
