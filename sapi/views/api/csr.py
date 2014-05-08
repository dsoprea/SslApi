import logging
import re

import web
import web.webapi

import OpenSSL.crypto

_logger = logging.getLogger(__name__)


class CsrApi(object):
    def POST(self):
        content_type = web.ctx.env['CONTENT_TYPE']

        if content_type != 'application/x-pem-file':
            raise web.webapi.HTTPError('403 Content-type not acceptable')

        csr_pem = web.data()

        csr = OpenSSL.crypto.load_certificate_request(
                OpenSSL.crypto.FILETYPE_PEM, 
                csr_pem)

        # Match for an extension like:
        #
        #   DNS:www.foo.com, DNS:www.bar.org, IP Address:192.168.1.1, IP Address:192.168.69.144, email:email@me
        #

        p = re.compile('^([a-zA-Z ]+:[^,]+, )+[a-zA-Z ]+:.+$')
        i = 0
        for extension in csr.get_extensions():
            e = str(extension)
            if p.match(e) is None:
                continue

            parts = [phrase.split(':') for phrase in e.split(', ')]
            _logger.debug("PARTS: %s" % (parts,))
