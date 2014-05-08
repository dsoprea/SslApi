import logging

import M2Crypto.X509
import M2Crypto.EVP

import sapi.ssl.utility

_logger = logging.getLogger(__name__)

def new_csr(private_key_pem, name, passphrase=None):
    _logger.debug("Creating request.")

    rsa = sapi.ssl.utility.pem_private_to_rsa(
            private_key_pem, 
            passphrase=passphrase)

    pkey = M2Crypto.EVP.PKey()
    pkey.assign_rsa(rsa)
    rsa = None # should not be freed here

    csr = M2Crypto.X509.Request()
    csr.set_pubkey(pkey)
    csr.set_subject(name)

    csr.sign(pkey, 'sha1')

    return csr.as_pem()

