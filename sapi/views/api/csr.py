import web


class CsrApi(object):
    def POST(self):
# TODO(dustin): Receive a CSR, authenticate that they've added an extension 
#               that will allow us to authenticate it to a client record.
        raise web.webapi.HTTPError('403 Forbidden')
