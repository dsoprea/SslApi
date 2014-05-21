Overview
--------

This is a CA that can sign CSRs, and make callbacks during each phase of the 
process. 

These callbacks allow you to:

1. Authenticate the signing request (API_CSR_AUTHORIZE_HOOK).
2. Make last-minute adjustments to the M2Crypto certificate object before 
   signing (like adding extensions) (API_CSR_PRESIGN_HOOK).
3. See the signed certificate before being returned (if you'd like to record 
   the certificate fingerprint, record the public-key, etc..) 
   (API_CSR_POSTSIGN_HOOK).


Design Philosophy
----------------

- A useful and obvious, callback-driven design.
- Simple adoption.

  This means that we need to be able to adopt users' existing keys. This also 
  meant that we couldn't impose the use of a database. Not only does a DB
  require an import and export tool, but this begins to obscure where the CA 
  certificate/keys reside in the system, and how to allow the API to handle 
  them without accidentally damaging or overwriting them.


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
