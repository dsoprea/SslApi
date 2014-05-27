import logging
import os
import os.path
import getpass
import sys

import M2Crypto.X509
import M2Crypto.EVP
import M2Crypto.X509

import sapi.config.ca
import sapi.ssl.utility
import sapi.ssl.certs
import sapi.ssl.helper
import sapi.exceptions

_CA_PASSPHRASE_CTX_READ = 'read'
_CA_PASSPHRASE_CTX_WRITE = 'write'
_CA_PASSPHRASE_ENV_NAME = 'CA_PASSPHRASE'

_logger = logging.getLogger(__name__)

_passphrase = None

def _get_passphrase():
    global _passphrase

    if _passphrase is None:
        try:
            passphrase = os.environ[_CA_PASSPHRASE_ENV_NAME]
        except KeyError:
            _logger.debug("We need to ask the user for the CA passphrase (not "
                          "available from the environment: [%s]).", 
                          _CA_PASSPHRASE_ENV_NAME)

            if sys.stdout.isatty() is False:
                raise EnvironmentError("A passphrase was not found in the "
                                       "environment, and we're not running in "
                                       "a terminal.")

            sys.stderr.write('\n')

            prompt = "CA passphrase for key: "
            passphrase = getpass.getpass(prompt, sys.stderr)

            if passphrase.strip() == '':
                raise ValueError("You must enter a passphrase.")

            prompt = "CA passphrase for key (again): "
            passphrase2 = getpass.getpass(prompt, sys.stderr)

            if passphrase2 != passphrase:
                raise ValueError("The passphrases don't agree.")

            sys.stderr.write('\n')
        else:
            _logger.debug("Passphrase retrieved from the environment: [%s]", 
                          _CA_PASSPHRASE_ENV_NAME)

        _passphrase = passphrase
    else:
        _logger.debug("We already have the passphrase.")

    return _passphrase


class _CA(object):
    """This class encapsulates CA operations. This class requires a complete CA 
    identity to already be build and available.
    """

    def __init__(self):
        _logger.debug("Loading CA: %s", sapi.config.ca.CA_PATH)

        self.__passphrase = _get_passphrase()

# TODO(dustin): We've had garbage-collection/memory issues with creating the 
#               RSA object here so that we don't keep having to reprocess the 
#               PEM.
        pem_cert_filepath = os.path.join(
                                sapi.config.ca.CA_PATH, 
                                sapi.config.ca.FILENAME_PEM_CERTIFICATE)

        with open(pem_cert_filepath) as f:
            self.__ca_cert_pem = f.read()

        pem_private_key_filepath = os.path.join(
                                    sapi.config.ca.CA_PATH, 
                                    sapi.config.ca.FILENAME_PEM_PRIVATE_KEY)

        with open(pem_private_key_filepath) as f:
            self.__ca_private_key_pem = f.read()

    def sign(self, csr_pem, validity_td, presign_hook_cb=None):
        _logger.debug("Signing request.")

        ca_cert = sapi.ssl.utility.pem_certificate_to_x509(self.__ca_cert_pem)

# TODO(dustin): Validate the DN fields in the CSR.
#        return sapi.config.ca.REQUIRED_DN_FIELDS.issubset(set(fields.keys()))

        return sapi.ssl.certs.new_cert(
                self.__ca_private_key_pem,
                csr_pem, 
                validity_td, 
                ca_cert.get_issuer(),
                passphrase=self.__passphrase,
                presign_hook_cb=presign_hook_cb)

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

_ca_instance = None

def ca_factory():
# TODO(dustin): We needed to manage a passphrase cache here, but no longer 
#               have to. Remove the factory?
    global _ca_instance

    if _ca_instance is None:
        _ca_instance = _CA()

    return _ca_instance

def generate_ca_identity(name, validity_td):
    _logger.info("Generating CA identity.")

    passphrase = _get_passphrase()
    return sapi.ssl.helper.new_selfsigned_cert(
            name, 
            passphrase, 
            validity_td, 
            bits=sapi.config.ca.BITS, 
            is_ca=True)

def write_identity(ca_private_key_pem, ca_public_key_pem, ca_csr_pem,
                   ca_cert_pem):
    """Write identity files."""

    private_key_filepath = os.path.join(
                            sapi.config.ca.CA_PATH, 
                            sapi.config.ca.FILENAME_PEM_PRIVATE_KEY)

    public_key_filepath = os.path.join(
                            sapi.config.ca.CA_PATH, 
                            sapi.config.ca.FILENAME_PEM_PUBLIC_KEY)

    csr_filepath = os.path.join(
                    sapi.config.ca.CA_PATH, 
                    sapi.config.ca.FILENAME_PEM_CSR)

    certificate_filepath = os.path.join(
                            sapi.config.ca.CA_PATH, 
                            sapi.config.ca.FILENAME_PEM_CERTIFICATE)

    if os.path.exists(private_key_filepath) is True or \
       os.path.exists(public_key_filepath) is True or \
       os.path.exists(csr_filepath) is True or \
       os.path.exists(certificate_filepath) is True:
        print("One or more of the following identity files is about to be "
              "overwritten:\n")

        print("CA private key: %s" % (private_key_filepath))
        print("CA public key: %s" % (public_key_filepath))
        print("CA csr: %s" % (csr_filepath))
        print("CA certificate: %s" % (certificate_filepath))

        print("\nAre you sure that you'd like to do this?")
        choice = raw_input('[y/N]? ')
        print('')

        choice = choice.strip()[:1].lower()

        if choice == '':
            choice = 'n'

        if choice != 'y':
            _logger.info("Identity update cancelled by user.")
            raise sapi.exceptions.CaUpdateCancelledException("Identity update cancelled.")

    _logger.info("Writing CA identity.")

    _logger.info("Writing CA PEM private-key: %s", private_key_filepath)

    with open(private_key_filepath, 'w') as f:
        f.write(ca_private_key_pem)

    _logger.info("Writing CA PEM public-key: %s", public_key_filepath)

    with open(public_key_filepath, 'w') as f:
        f.write(ca_public_key_pem)

    _logger.info("Writing CA PEM CSR: %s", csr_filepath)

    with open(csr_filepath, 'w') as f:
        f.write(ca_csr_pem)

    _logger.info("Writing CA PEM certificate: %s", certificate_filepath)

    with open(certificate_filepath, 'w') as f:
        f.write(ca_cert_pem)
