import logging
import datetime

_logger = logging.getLogger(__name__)

def _api_csr_authorize_hook(csr, subject_alt_name_exts):
    """This will be called whenever a CSR has been submitted for signing.
    As a convenience, the subjectAlternativeName extension data has already 
    been retrieved and passed as an argument.

    If this CSR either violates your policies or you can't extract any
    identifying information that might be required in a
    subjectAlternativeName extension, raise sapi.exceptions.CsrSignError and
    provide a meaningful error message.
    """

    _logger.info("CSR authorize hook.")
    return datetime.timedelta(days=365)

API_CSR_AUTHORIZE_HOOK = _api_csr_authorize_hook
