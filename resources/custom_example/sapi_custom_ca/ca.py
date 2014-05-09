import os
import os.path

DEFAULT_PATH = '/tmp/sapi/ca'

if os.path.exists(DEFAULT_PATH) is False:
    os.makedirs(DEFAULT_PATH)
