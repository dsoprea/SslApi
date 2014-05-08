import logging

import M2Crypto.RSA

import sapi.ssl.utility

_logger = logging.getLogger(__name__)

def new_key(passphrase=None, bits=2048):
    _logger.debug("Creating keys.")

    # This is called during key-generation to provide visual feedback. The 
    # default callback shows progress dots.
    def progress_cb(arg1, arg2):
        pass

    rsa = M2Crypto.RSA.gen_key(bits, 65537, progress_cb)

    private_key_pem = sapi.ssl.utility.rsa_to_pem_private(rsa, passphrase)
    public_key_pem = sapi.ssl.utility.rsa_to_pem_public(rsa)

    return (private_key_pem, public_key_pem)
