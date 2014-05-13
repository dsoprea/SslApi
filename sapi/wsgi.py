import sapi.app.main
import sapi.ssl.ca

# Induce the CA passphrase to be asked and remembered.
sapi.ssl.ca.ca_factory()

wsgi = sapi.app.main.app.wsgifunc()
