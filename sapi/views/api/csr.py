import logging
import re
import hashlib
import collections

import web
import web.webapi

import M2Crypto.X509
import OpenSSL.crypto

#import pyasn1.codec.der.decoder
#import pyasn1_modules.rfc2314
#import pyasn1_modules.rfc2459

import sapi.config.api.server
import sapi.config.ca
import sapi.exceptions
import sapi.ssl.utility
import sapi.ssl.ca

_logger = logging.getLogger(__name__)


class CsrApi(object):
    def PUT(self, client_hash):
        _logger.debug("Signing certificate for client: %s", client_hash)

        content_type = web.ctx.env['CONTENT_TYPE']

        if content_type != 'application/x-pem-file':
            raise web.webapi.HTTPError('403 Content-type not acceptable')

        csr_pem = web.data()

        csr_m = M2Crypto.X509.load_request_string(csr_pem)

        csr_o = OpenSSL.crypto.load_certificate_request(
                    OpenSSL.crypto.FILETYPE_PEM, 
                    csr_pem)

        # Match for an extension like:
        #
        #   DNS:www.foo.com, DNS:www.bar.org, IP Address:192.168.1.1, IP Address:192.168.69.144, email:email@me
        #

        p = re.compile('^([a-zA-Z ]+:[^,]+, )+[a-zA-Z ]+:.+$')
        i = 0
        subject_alt_name_exts = []
        for extension in csr_o.get_extensions():
            e = str(extension)
            if p.match(e) is None:
                continue

            parts = [phrase.split(':') for phrase in e.split(', ')]

            subject_alt_name_exts.append(parts)

        # Calculate a hash that can be used to refer to this CSR with the 
        # callbacks.
        public_key_hash = sapi.ssl.utility.hash_from_public_key(
                            csr_m.get_pubkey())

        csr_t = collections.namedtuple(
                    'CsrTuple', 
                    ['csr_m', 'csr_o', 'csr_pem'])

        csr_tuple = csr_t(csr_m, csr_o, csr_pem)

        hooks = sapi.config.api.server.API_CSR_HOOKS_FACTORY(
                    client_hash, 
                    public_key_hash, 
                    csr_tuple)

        try:
            validity_td = hooks.authorize(subject_alt_name_exts)
        except sapi.exceptions.CsrNotAuthedError as e:
            _logger.warn("Signing has been refused for CSR with public-key "
                         "[%s]: %s", 
                         public_key_hash, e)
            raise web.webapi.HTTPError('403 Signing not authorized.')

        ca = sapi.ssl.ca.ca_factory()

        def presign_hook_cb(cert, csr_pem):
            hooks.presign(cert)

        cert_pem = ca.sign(
                    csr_pem, 
                    validity_td, 
                    presign_hook_cb=presign_hook_cb)

        cert = sapi.ssl.utility.pem_certificate_to_x509(cert_pem)
        hooks.postsign(cert)

        return { 'signed_x509_pem': cert_pem }
