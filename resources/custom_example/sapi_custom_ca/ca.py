import os
import os.path
import logging

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
    print("Presign hook!")

CSR_PRESIGN_HOOK = _csr_presign_hook
