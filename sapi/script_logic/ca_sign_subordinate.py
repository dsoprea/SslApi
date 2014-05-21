import sys

import datetime
import logging
import argparse
import os
import hashlib

import M2Crypto.X509

#import sapi.config.log
import sapi.utility
import sapi.ssl.ca
import sapi.ssl.utility

_logger = logging.getLogger(__name__)

def start():
    description = "Sign subordinate CSR."

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-f', '--csr_filepath',
                        metavar='filepath',
                        help="The filepath of the CSR (defaults to STDIN)")

    parser.add_argument('-o', '--out_filepath',
                        metavar='filepath',
                        help="The filepath of the new certificate (defaults to STDOUT)")

    parser.add_argument('validity',
                        metavar='validity',
                        help="The validity duration (can suffix 's' (seconds), "\
                             "'d' (days), 'y' (years, the default))")

    args = parser.parse_args()

    # Validate/distill arguments.

    validity = sapi.utility.get_delta_from_validity_phrase(args.validity)

    if args.csr_filepath is not None:
        with open(args.csr_filepath) as f:
            csr_pem = f.read()
    else:
        csr_pem = sys.stdin.read()

    # Build the identity artifacts.

    _logger.debug("Signing request.")

    ca = sapi.ssl.ca.ca_factory()

    def presign_hook_cb(cert, csr_pem):
        public_key_hash = sapi.ssl.utility.hash_from_public_key(cert.get_pubkey())
        sapi.config.ca.CSR_PRESIGN_HOOK(cert, public_key_hash)

    cert_pem = ca.sign(csr_pem, validity, presign_hook_cb=presign_hook_cb)

    if args.out_filepath is not None:
        with open(args.out_filepath, 'w') as f:
            f.write(cert_pem)
    else:
        sys.stdout.write(cert_pem)
