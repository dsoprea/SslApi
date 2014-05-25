import logging

import sapi.config.ca
import sapi.utility
import sapi.config.api.signing_hooks_base

_logger = logging.getLogger(__name__)

API_CSR_HOOKS_FACTORY = lambda client_hash, public_key_hash, csr_tuple:
                            return sapi.config.api.signing_hooks_base.SigningHooksBase(
                                          client_hash, 
                                          public_key_hash, 
                                          csr_tuple)
