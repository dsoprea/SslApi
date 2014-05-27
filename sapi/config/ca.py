import os
import os.path
import logging
import hashlib
import time
import random

_logger = logging.getLogger(__name__)

FILENAME_PEM_PRIVATE_KEY = 'ca.private_key.pem'
FILENAME_PEM_PUBLIC_KEY = 'ca.public_key.pem'
FILENAME_PEM_CSR = 'ca.csr.pem'
FILENAME_PEM_CERTIFICATE = 'ca.cert.pem'

REQUIRED_DN_FIELDS = set(('C', 'ST', 'L', 'O', 'CN', 'emailAddress'))
BITS = 2048

CA_PATH = os.environ.get('SAPI_CA_PATH', '/var/lib/ca')

DEFAULT_VALIDITY_Y = 10
DEFAULT_SUBORDINATE_VALIDITY_Y = 1

_logger.debug("Importing custom API hooks (CA, optional).")

# Technically, this should be unique to the CA. SHA1 will be sufficient as a 
# default implementation.
SERIAL_NUMBER_GENERATOR_CB = lambda: \
                                hashlib.sha1(str(time.time()) + str(random.random())).\
                                    hexdigest()

CUSTOM_BOOT_CB = lambda: None

try:
    from sapi_custom_ca.ca import *
except ImportError:
    _logger.debug("Custom functionality not found (CA).")
else:
    _logger.debug("Custom functionality found (CA).")
    CUSTOM_BOOT_CB()

_logger.info("CA PATH: %s", CA_PATH)

if os.path.exists(CA_PATH) is False:
    os.makedirs(CA_PATH)
