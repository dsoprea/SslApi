#!/usr/bin/env python2.7

import sys
import os.path

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, root_path)

import datetime
import logging
import argparse
import os

import M2Crypto.X509

import sapi.config.ca
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

    FMT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(FMT)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

#_configure_logging()
_logger = logging.getLogger(__name__)

description = "Create CA keys and certificate."

parser = argparse.ArgumentParser(description=description)

parser.add_argument('ca_path',
                    default='/var/lib/ca',
                    metavar='path',
                    help='The path to install the CA identity files to')

parser.add_argument('-p', '--passphrase',
                    metavar='passphrase',
                    help='The passphrase for the new private-key (will be '\
                         'prompted if not given)')

parser.add_argument('-b', '--bits',
                    type=int,
                    default=2048,
                    metavar='bits',
                    help='The passphrase for the new private-key (will be '\
                         'prompted if not given)')

parser.add_argument('-f', '--field',
                    action='append',
                    nargs=2,
                    metavar=('key','value'),
                    required=True,
                    help='A distinguished-name field (C, ST, L, O, OU, '\
                         'CN, emailAddress, etc..) and value')

parser.add_argument('-d', '--duration',
                    default='10',
                    metavar='duration',
                    help="The validity duration (can suffix 's' (seconds), "\
                         "'d' (days), 'y' (years, the default))")

args = parser.parse_args()

duration = args.duration
def _translate_years_to_seconds(years):
    now_dt = datetime.datetime.now()
    now_future_dt = now_dt.replace(year=(now_dt.year + years))
    return (now_future_dt - now_dt).total_seconds()

try:
    duration = int(duration)
except ValueError:
    if duration == '':
        raise ValueError("Duration is empty.")
    
    suffix = duration[-1].lower()
    duration = int(duration[:-1])

    if suffix == 'y':
        duration = _translate_years_to_seconds(years)
    elif suffix == 'd':
        duration = duration * 86400
    elif suffix != 's':
        raise ValueError("Duration suffix [%s] not valid. Please use 's', "
                         "'d', or 'y'.")
else:
    duration = _translate_years_to_seconds(duration)

if args.passphrase is None:
    print("Please enter the passphrase:")
    passphrase = raw_input()
    if passphrase.strip() == '':
        raise ValueError("Please enter a passphrase.")

    print("Please enter the passphrase (again):")
    passphrase2 = raw_input()
    if passphrase2 != passphrase:
        raise ValueError("Passphrases don't match.")
else:
    passphrase = args.passphrase

# Load the DB fields. As we're building the CA, don't check them (assume the 
# user entered what they considered to be acceptable).

name = M2Crypto.X509.X509_Name()
for (k, v) in args.field:
    try:
        M2Crypto.X509.X509_Name.nid[k]
    except KeyError as e:
        raise ValueError("DN field is not valid: [%s]" % (k))

    setattr(name, k, v)

duration = datetime.timedelta(seconds=365 * 86400)

print("Generating CA identity.")

identity = sapi.ssl.helper.new_selfsigned_cert(
            name, 
            passphrase, 
            duration, 
            bits=args.bits, 
            is_ca=True)

(ca_private_key_pem, ca_public_key_pem, ca_cert_pem) = identity

if os.path.exists(args.ca_path) is True:
    raise EnvironmentError("CA path [%s] already exists. Please choose a "
                           "directory that can be created." % (args.ca_path))

os.makedirs(args.ca_path)

private_key_filepath = os.path.join(
                        args.ca_path, 
                        sapi.config.ca.FILENAME_PEM_PRIVATE_KEY)

print("Writing CA PEM private-key: %s" % (private_key_filepath))

with open(private_key_filepath, 'w') as f:
    f.write(ca_private_key_pem)

public_key_filepath = os.path.join(
                        args.ca_path, 
                        sapi.config.ca.FILENAME_PEM_PUBLIC_KEY)

print("Writing CA PEM public-key: %s" % (public_key_filepath))

with open(public_key_filepath, 'w') as f:
    f.write(ca_public_key_pem)

certificate_filepath = os.path.join(
                        args.ca_path, 
                        sapi.config.ca.FILENAME_PEM_CERTIFICATE)

print("Writing CA PEM certificate: %s" % (certificate_filepath))

with open(certificate_filepath, 'w') as f:
    f.write(ca_cert_pem)
