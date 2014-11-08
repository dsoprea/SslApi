import logging

import sapi.config.log
import sapi.app.main
import sapi.ssl.ca

_logger = logging.getLogger(__name__)

# Induce the CA passphrase to be asked and remembered.
sapi.ssl.ca.ca_factory()

print("CA webserver booting.")

wsgi = sapi.app.main.app.wsgifunc()
