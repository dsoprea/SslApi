import logging
import os.path

import M2Crypto.X509
import M2Crypto.EVP
import M2Crypto.X509

import sapi.config.ca
import sapi.ssl.utility
import sapi.ssl.certs

_logger = logging.getLogger(__name__)


class CA(object):
    def __init__(self, ca_path, passphrase):
        _logger.debug("Loading CA: %s", ca_path)

# TODO(dustin): We've had garbage-collection/memory issues with creating the 
#               RSA object here so that we don't keep having to reprocess the 
#               PEM.
        pem_cert_filepath = os.path.join(
                                ca_path, 
                                sapi.config.ca.FILENAME_PEM_CERTIFICATE)

        with open(pem_cert_filepath) as f:
            self.__ca_cert_pem = f.read()

        pem_private_key_filepath = os.path.join(
                                    ca_path, 
                                    sapi.config.ca.FILENAME_PEM_PRIVATE_KEY)

        with open(pem_private_key_filepath) as f:
            self.__ca_private_key_pem = f.read()

        self.__passphrase = passphrase

    def sign(self, csr_pem, validity):
        _logger.debug("Signing request.")

        ca_cert = sapi.ssl.utility.pem_certificate_to_x509(self.__ca_cert_pem)

# TODO(dustin): Validate the DN fields in the CSR.
#        return sapi.config.ca.REQUIRED_DN_FIELDS.issubset(set(fields.keys()))

        return sapi.ssl.certs.new_cert(
                self.__ca_private_key_pem,
                csr_pem, 
                validity, 
                ca_cert.get_issuer(),
                passphrase=self.__passphrase)

#class CRL(object):
#3 TODO(dustin): How do we use this data?
## TODO(dustin): How do we initialize this data (currently, we create an empty 
##               file, but we don't know if that'll work).
#    def __init__(self, crl_filepath):
#        if os.path.isfile(crl_filepath) is False:
#            with open(crl_filepath, 'w') as f:
#                pass
#
#        self.__crl = M2Crypto.CRL.load_crl(crl_filepath)
