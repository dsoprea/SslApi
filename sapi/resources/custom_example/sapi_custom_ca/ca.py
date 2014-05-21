import os
import os.path
import logging

import M2Crypto.X509

_logger = logging.getLogger(__name__)

root_path = os.path.abspath(os.path.join(
                os.path.dirname(__file__), 
                '..', 
                '..', 
                '..'))

DEFAULT_PATH = ('%s/dev/ca' % (root_path))

if os.path.exists(DEFAULT_PATH) is False:
    os.makedirs(DEFAULT_PATH)

def _csr_presign_hook(cert, public_key_hash):
#    ext = M2Crypto.X509.new_extension('subjectAltName', 'email:abc@def.com')
#    cert.add_ext(ext)
    pass

CSR_PRESIGN_HOOK = _csr_presign_hook
