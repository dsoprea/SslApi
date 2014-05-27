Overview
--------

This is a certificate authority API that can sign CSRs, and make callbacks 
during each phase of the process. 

These callbacks allow you to:

1. Authenticate the signing request (API_CSR_AUTHORIZE_HOOK).
2. Make last-minute adjustments to the M2Crypto certificate object before 
   signing (like adding extensions or setting the certificate version) 
   (API_CSR_PRESIGN_HOOK).
3. See the signed certificate before being returned (if you'd like to record 
   the certificate fingerprint, record the public-key, etc..) 
   (API_CSR_POSTSIGN_HOOK).


Design Philosophy
----------------

- Useful and intuitive callback-driven design.
- Accomodate customization/callbacks without modifying SSL API project.
- Simple adoption.

  This means that we need to be able to adopt users' existing keys. This also 
  meant that we couldn't impose the use of a database. Not only does a DB
  require an import and export tool, but this begins to obscure where the CA 
  certificate/keys reside in the system, and how to allow the API to handle 
  them without accidentally damaging or overwriting them.


Server Setup
------------

1. Install *ssl_api*:

    $ sudo pip install ssl_api

2. Create the directory for the CA's own certificate/keys (referred to as the 
   "identity").

    $ sudo mkdir /var/lib/ca

3. Establish the CA identity.

   If you need to create a new identity (the "v" parameter describes the 
   validity time-period to be valid for, and defaults to ten-years):

    $ sudo ca_create_identity \
        -f C US \
        -f CN ca.net \
        -f L "Palm Beach" \
        -f O "Random Authority, Inc." \
        -f ST Florida \
        -f emailAddress ca@openpeak.com \
        -v 10

   If you already have certificates/keys, copy them to */var/lib/ca* as:

   - ca.cert.pem
   - ca.csr.pem
   - ca.private_key.pem
   - ca.public_key.pem

4. Create the user and update identity permissions.

   1. sudo adduser --disabled-password --disabled-login --gecos "" --no-create-home ca 
   2. sudo adduser root ca
   3. sudo chown root.ca -R /var/lib/ca
   4. sudo chmod 750 /var/lib/ca
   5. sudo chmod 640 -R /var/lib/ca/*


Configuring Startup
-------------------

It is assumed that you're going to want to start the CA at every system 
startup. However, the CA private-key requires a passphrase to be entered.

For your convenience, a passphrase will only be requested from the terminal


Random Details
--------------

- The default length of the CA key is 2048-bits.


Compatibility
-------------

As this project uses web.py, it is only compatible with Python 2.x .


Unsupported functionalities
---------------------------

- We do not directly support the CRL (or OCSP, etc..). It'll be up to the 
  developer to add a CDP (CRL distribution point) from the pre-signing 
  callback, and then to host it themselves.


Disclaimer
----------

Though functional, this project must undergo a final review before being officially documented.
