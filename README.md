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

  Callbacks are triggered at various phases of the signing processes.

- Accomodate customization/callbacks without modifying SSL API project.

  Adjust CA behavior from a shell-project and not the *ssl_api* code.

- Simple adoption.

  This means that we need to be able to adopt users' existing keys. This also 
  meant that we couldn't impose the use of a database. Not only does a DB
  require an import and export tool, but this begins to obscure where the CA 
  certificate/keys reside in the system, and how to allow the API to handle 
  them without accidentally damaging or overwriting them.


Server Setup
------------

1. Install *ssl_api*:
    
    ```
    $ sudo pip install ssl_api
    ```

2. Create the directory for the CA's own certificate/keys (referred to as the 
   "identity").

    ```
    $ sudo mkdir /var/lib/ca
    ```

3. Establish the CA identity.
   
   If you need to create a new identity (the "v" parameter describes the 
   validity time-period to be valid for, and defaults to ten-years):

    ```
    $ sudo ca_create_identity \
        -f C US \
        -f CN ca.net \
        -f L "Palm Beach" \
        -f O "Random Authority, Inc." \
        -f ST Florida \
        -f emailAddress ca@openpeak.com \
        -v 10
    ```

    This creates the following files at the identity path: 

      *ca.cert.pem*, *ca.csr.pem*, *ca.private_key.pem*, *ca.public_key.pem*

   If you already have certificates/keys, copy them to the identity path with 
   the same names as the above.

4. Create the user and update identity permissions.

   ```
   $ sudo adduser --disabled-password --disabled-login --gecos "" --no-create-home ca 
   $ sudo adduser root ca
   $ sudo chown root.ca -R /var/lib/ca
   $ sudo chmod 750 /var/lib/ca
   $ sudo chmod 640 -R /var/lib/ca/*
   ```

5. Start the server immediately by running one of the following:

   - Start in the foreground with debugging:

     ```
     $ ca_start_gunicorn_dev
     ```

   - Start in the background without debugging, with the right user, etc..:

     ```
     CA_PASSPHRASE=test ca_start_gunicorn_prod
     ```

   A passphrase is required. If it is not found as "CA_PASSPHRASE" in the
   environment, the user will be prompted. See the next section ("Startup") 
   for details.
   

Notes on Automatic Startup
--------------------------

It is assumed that you're going to want to start the CA at every system 
startup. However, the CA private-key requires a passphrase to be entered.

For your convenience, the passphrase may be set as an environment variable 
named "CA_PASSPHRASE". A passphrase will only be requested from the terminal if 
one is not found in the environment. An EnvironmentError will be raised in the 
event that a passphrase is not in the environment and the server is not being 
launched in a terminal.

*ssl_api* ships with two Gunicorn configurations (in sapi/resources/data):

- gunicorn.conf.dev
- gunicorn.conf.prod

The main difference is whether the terminal remains attached to the server or 
not. 

If you use the default production Gunicorn configuration, you'll be required to
set your passphrase via the environment variable, since the server will 
daemonize. If you wish to be prompted, you'll either have to use the development 
configuration, or modify the production config to set "daemon" to "'false'" (it 
must be expressed in quotes, in the file).

It is left to the administrator to start the server using whichever method he 
likes (such as using /etc/rc.local or Upstart).


Implementing Callbacks and Other Custom Configuration
-----------------------------------------------------

(needs to be finished)


Other Details
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

This project (and its documentation) is currently approaching final release. As 
such it is still subject to change (probably not by much, though)
