import logging

import sapi.config.ca
import sapi.utility

_logger = logging.getLogger(__name__)


class SigningHooksBase(object):
    def __init__(self, client_hash, public_key_hash, csr_tuple):
        self.__client_hash = client_hash
        self.__public_key_hash = public_key_hash
        self.__csr_tuple = csr_tuple

        _logger.debug("Initializing default CSR hooks.")

    def authorize(self, subject_alt_name_exts):
        """At the top of the request, perhaps to verify the caller by the 
        client-hash or the information in the CSR. Return the validity length
        for the new cert, expressed as a timedelta.
        """

        validity_td = sapi.utility.get_delta_from_validity_phrase(
                         sapi.config.ca.DEFAULT_SUBORDINATE_VALIDITY_Y)

        return validity_td

    def presign(self, certificate):
        """Called with the certificate before it's signed, to add extensions 
        or such. Must return a CSR PEM.
        """

        pass

    def postsign(self, signed_certificate):
        """Called with the certificate after it's signed, perhaps to store the 
        certificate's fingerprint.
        """

        pass

    @property
    def client_hash(self):
        return self.__client_hash

    @property
    def public_key_hash(self):
        return self.__public_key_hash

    @property
    def csr_tuple(self):
        return self.__csr_tuple
