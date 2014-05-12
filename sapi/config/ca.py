FILENAME_PEM_PRIVATE_KEY = 'ca_private.pem'
FILENAME_PEM_PUBLIC_KEY = 'ca_public.pem'
FILENAME_PEM_CERTIFICATE = 'ca_cert.pem'

REQUIRED_DN_FIELDS = set(('C', 'ST', 'L', 'O', 'CN', 'emailAddress'))
BITS = 2048

DEFAULT_PATH = '/var/lib/ca'
DEFAULT_VALIDITY_Y = 10

CSR_PRESIGN_HOOK = lambda certificate, public_key_hash: None

try:
    from sapi_custom_ca.ca import *
except ImportError:
    pass
