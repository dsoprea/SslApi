import logging
import hashlib

import M2Crypto.BIO
import M2Crypto.RSA
import M2Crypto.X509

_logger = logging.getLogger(__name__)

def rsa_to_pem_private(rsa, passphrase=None):
    _logger.debug("Converting RSA object to private PEM string.")

    bio = M2Crypto.BIO.MemoryBuffer()

    private_key_kwargs = {}
    if passphrase is None:
        private_key_kwargs['cipher'] = None
    else:
        def passphrase_cb(arg1):
            return passphrase

        private_key_kwargs['callback'] = passphrase_cb

    rsa.save_key_bio(bio, **private_key_kwargs)
    return bio.read()

def rsa_to_pem_public(rsa):
    _logger.debug("Converting RSA object to public PEM string.")

    bio = M2Crypto.BIO.MemoryBuffer()
    rsa.save_pub_key_bio(bio)
    return bio.read()

def pem_private_to_rsa(private_key_pem, passphrase=None):
    _logger.debug("Converting private PEM to RSA object.")

    def passphrase_cb(*args):
        return passphrase

    rsa = M2Crypto.RSA.load_key_string(
            private_key_pem, 
            callback=passphrase_cb)

    return rsa

def pem_certificate_to_x509(cert_pem):
    _logger.debug("Converting PEM certificate to X509 object.")

    return M2Crypto.X509.load_cert_string(cert_pem)

def pem_csr_to_csr(csr_pem):
    _logger.debug("Converting PEM CSR to CSR object.")

    return M2Crypto.X509.load_request_string(csr_pem)

def hash_from_public_key(public_key):
    public_key_der = public_key.as_der()
    return hashlib.sha1(public_key_der).hexdigest()
