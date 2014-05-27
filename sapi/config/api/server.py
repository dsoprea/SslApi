import logging

import sapi.config.ca
import sapi.utility
import sapi.config.api.signing_hooks_base

_logger = logging.getLogger(__name__)

def _default_csr_hooks_factory(client_hash, public_key_hash, csr_tuple):
    return sapi.config.api.signing_hooks_base.SigningHooksBase(
            client_hash,
            public_key_hash,
            csr_tuple)

API_CSR_HOOKS_FACTORY = _default_csr_hooks_factory

try:
    from sapi_custom_ca.api import *
except ImportError:
    _logger.debug("Custom functionality not found (server).")
else:
    _logger.debug("Custom functionality found (server).")
