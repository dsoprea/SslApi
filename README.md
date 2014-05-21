Overview
--------

This is a CA that can sign CSRs, and make callbacks during each phase of the process. 

These callbacks allow you to:

1. Authenticate the signing request.
2. Make last-minute adjustments to the M2Crypto certificate object before signing (like adding extensions).
3. See the signed certificate before being returned (if you'd like to record the certificate fingerprint, record the public-key, etc..).

Disclaimer
----------

Though functional, this project must undergo a final review before being officially documented.
