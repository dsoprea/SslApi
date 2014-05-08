#!/usr/bin/env python2.7

import sys
import os.path

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, root_path)

import datetime
import logging

import M2Crypto.X509

import sapi.ssl.helper
import sapi.ssl.ca
import sapi.ssl.requests
import sapi.ssl.keys

def _configure_logging():
    # Configure logging.

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    #logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

#_configure_logging()
_logger = logging.getLogger(__name__)

def get_ca():
    PRIVATE_FILEPATH = 'ca_private.pem'
    PUBLIC_FILEPATH = 'ca_public.pem'
    CERT_FILEPATH = 'ca_cert.pem'

    passphrase = 'test'

    if os.path.exists(PRIVATE_FILEPATH) is False:
        _logger.debug("Creating CA identity")

        name = M2Crypto.X509.X509_Name()
        name.C = 'US'
        name.ST = 'Florida'
        name.L = 'Boca Raton'
        name.O = 'OpenPeak Inc.'
        name.CN = 'openpeak.com'
        name.emailAddress = 'ca@openpeak.com'

        duration = datetime.timedelta(seconds=365 * 86400)

        identity = sapi.ssl.helper.new_selfsigned_cert(name, passphrase, duration, is_ca=True)
        (ca_private_key_pem, ca_public_key_pem, ca_cert_pem) = identity

        with open(PRIVATE_FILEPATH, 'w') as f:
            f.write(ca_private_key_pem)

        with open(PUBLIC_FILEPATH, 'w') as f:
            f.write(ca_public_key_pem)

        with open(CERT_FILEPATH, 'w') as f:
            f.write(ca_cert_pem)

    _logger.debug("Loading CA identity")

    with open(PRIVATE_FILEPATH) as f:
        ca_private_key_pem = f.read()

    with open(PUBLIC_FILEPATH) as f:
        ca_public_key_pem = f.read()

    with open(CERT_FILEPATH) as f:
        ca_cert_pem = f.read()

    return sapi.ssl.ca.CA(ca_cert_pem, ca_private_key_pem, passphrase)

ca = get_ca()

#print(ca_private_key_pem)
#print(ca_public_key_pem)
#print(ca_cert_pem)

# Build a subordinate certificate.

pair = sapi.ssl.keys.new_key()
(private_key_pem, public_key_pem) = pair

name = M2Crypto.X509.X509_Name()
name.C = 'US'
name.ST = 'Florida'
name.L = 'Boca Raton'
name.O = 'OpenPeak Inc. 2'
name.CN = 'openpeak2.com'
name.emailAddress = 'subcert@openpeak.com'

csr_pem = sapi.ssl.requests.new_csr(
            private_key_pem, 
            name)

duration = datetime.timedelta(seconds=365 * 86400)
r = ca.sign(csr_pem, duration)
print(r)
