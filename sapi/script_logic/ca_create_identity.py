import sys

import datetime
import logging
import argparse
import os

import M2Crypto.X509

import sapi.config.ca
#import sapi.config.log
import sapi.utility
import sapi.ssl.helper
import sapi.ssl.ca
import sapi.ssl.requests
import sapi.ssl.keys
import sapi.exceptions

_logger = logging.getLogger(__name__)

def start():
    description = "Create CA keys and certificate."

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-f', '--field',
                        action='append',
                        nargs=2,
                        metavar=('key','value'),
                        required=True,
                        help='A distinguished-name field (C, ST, L, O, OU, '\
                             'CN, emailAddress, etc..) and value')

    parser.add_argument('-v', '--validity',
                        default=str(sapi.config.ca.DEFAULT_VALIDITY_Y),
                        metavar='validity',
                        help="The validity duration (can suffix 's' (seconds), "\
                             "'d' (days), 'y' (years, the default))")

    args = parser.parse_args()

    # Validate/distill arguments.

    validity = sapi.utility.get_delta_from_validity_phrase(args.validity)

    # Build the identity artifacts.

    dn = dict(args.field)
    name = sapi.utility.build_name_from_dict(**dn)

    print("Generating CA identity.")

    identity = sapi.ssl.ca.generate_ca_identity(name, validity)

    try:
        sapi.ssl.ca.write_identity(*identity)
    except sapi.exceptions.CaUpdateCancelledException:
        print("CA identity update cancelled.")
        sys.exit(1)

    print("CA identity written.")
