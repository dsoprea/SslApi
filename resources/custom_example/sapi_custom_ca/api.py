import logging
import datetime

_logger = logging.getLogger(__name__)

# An example to show how to store information between callbacks.
_signed_cache = {}

def _api_csr_authorize_hook(subject_alt_name_exts, csr_tuple, public_key_hash,
                            client_hash):
    """This will be called whenever a CSR has been submitted for signing.
    As a convenience, the subjectAlternativeName extension data has already 
    been retrieved, parsed, and passed as an argument.

    'client_hash' is the hash provided to the signing API call in the URL.

    If this CSR either violates your policies or you can't extract any
    identifying information that might be required in a
    subjectAlternativeName extension, raise sapi.exceptions.CsrSignError and
    provide a meaningful error message.

    The public_key_hash can be used to track this CSR between callbacks. It can
    be combined with the CSR version and be used to bind the CSR to an existing 
    or expired certificate in your system.

    Return a timedelta representing the validity range for the certificate.
    """

# TODO(dustin): We need to keep track of the last certificate serial number. 
#               The certificate being used for an API request must be using 
#               that serial number.

    _logger.info("Extensions:\n%s", subject_alt_name_exts)

    # Store some stuff for subsequent callbacks. Note that it's guaranteed that 
    # the other callback will be called and can clean this up.
    _signed_cache[public_key_hash] = subject_alt_name_exts

    return datetime.timedelta(days=365)

API_CSR_AUTHORIZE_HOOK = _api_csr_authorize_hook

def _api_csr_postsign_hook(cert, public_key_hash):
    """The CSR has been signed. You might create a record in your system with 
    the DN, certificate fingerprint, public-key hash, and version (so that you 
    know if they use the most recent certificate or not), now."""

    # Recover the subjectAltName information in order to grab the token 
    # required by our company in order to store it with the record.
    subject_alt_name_exts = _signed_cache[public_key_hash]
    del _signed_cache[public_key_hash]

    fingerprint = cert.get_fingerprint(md='md5')
    _logger.info("Cert fingerprint: %s", fingerprint)

API_CSR_POSTSIGN_HOOK = _api_csr_postsign_hook
