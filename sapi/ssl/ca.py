import logging

import M2Crypto.X509
import M2Crypto.EVP
import M2Crypto.X509

import sapi.ssl.utility
import sapi.config.ca

_logger = logging.getLogger(__name__)


class CA(object):
    def __init__(self, ca_cert_pem, ca_private_key_pem, passphrase):
        _logger.debug("Initializing CA.")

# TODO(dustin): We've had garbage-collection/memory issues with creating the 
#               RSA object here so that we don't keep having to reprocess the 
#               PEM.
        self.__ca_cert_pem = ca_cert_pem
        self.__ca_private_key_pem = ca_private_key_pem
        self.__passphrase = passphrase

    def sign(self, csr_pem, duration):
        _logger.debug("Signing request.")

        ca_cert = sapi.ssl.utility.pem_certificate_to_x509(self.__ca_cert_pem)
        issuer_name = ca_cert.get_issuer()

        return sapi.ssl.certs.new_cert(
                self.__ca_private_key_pem,
                csr_pem, 
                duration, 
                issuer_name,
                passphrase=self.__passphrase)

    def check_for_required_dn_fields(self, fields):
        return sapi.config.ca.REQUIRED_DN_FIELDS.issubset(set(fields.keys()))

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
