import logging

_logger = logging.getLogger(__name__)

API_CSR_AUTHORIZE_HOOK = None
API_CSR_POSTSIGN_HOOK = lambda cert: None

from sapi_custom_ca.api import *

if API_CSR_AUTHORIZE_HOOK is None:
    raise EnvironmentError("API_CSR_AUTHORIZER must be configured.")
