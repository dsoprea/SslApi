import logging

import M2Crypto.X509

import sapi.ssl.keys
import sapi.ssl.requests
import sapi.ssl.certs

_logger = logging.getLogger(__name__)

def new_selfsigned_cert(issuer_name, passphrase, validity_td, bits=2048, 
                        is_ca=False):
    _logger.debug("Creating self-signed certificate. IS_CA=[%s]", is_ca)

    pair = sapi.ssl.keys.new_key(passphrase)
    (private_key_pem, public_key_pem) = pair

    csr_pem = sapi.ssl.requests.new_csr(
                private_key_pem, 
                issuer_name, 
                passphrase=passphrase)

#    issuer_name = M2Crypto.X509.X509_Name()
#
## TODO(dustin): We're still waiting for a response on whether setting 
##               issuer-subject==request-subject is reasonable.
#    issuer_name.C = name.C
#    issuer_name.ST = name.ST
#    issuer_name.L = name.L
#    issuer_name.O = name.O
#    issuer_name.CN = name.CN

    cert_pem = sapi.ssl.certs.new_cert(
                private_key_pem, 
                csr_pem, 
                validity_td, 
                issuer_name, 
                passphrase=passphrase,
                is_ca=is_ca)

    return (private_key_pem, public_key_pem, csr_pem, cert_pem)
