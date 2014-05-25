import logging

_logger = logging.getLogger(__name__)

# At the top of the request, perhaps to verify the caller by the client-hash or 
# the information in the CSR.
API_CSR_AUTHORIZE_HOOK = lambda \
                            subject_alt_name_exts, \
                            csr_tuple, \
                            public_key_hash, \
                            client_hash: None

# Called with the certificate before it's signed, to add extensions or such. 
# Must return a CSR PEM.
API_CSR_PRESIGN_HOOK = lambda \
                            csr_tuple, \
                            certificate, \
                            public_key_hash, \
                            client_hash: csr_tuple.csr_pem

# Called with the certificate after it's signed, perhaps to store the 
# certificate's fingerprint.
API_CSR_POSTSIGN_HOOK = lambda \
                            certificate, \
                            public_key_hash, \
                            client_hash: None

_logger.debug("Importing custom API hooks (required).")
from sapi_custom_ca.api import *
