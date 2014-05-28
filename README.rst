.. image:: https://pypip.in/d/ssl_api/badge.png
    :target: https://pypi.python.org/pypi/ssl_api/
    :alt: Downloads

.. image:: https://pypip.in/v/ssl_api/badge.png
    :target: https://pypi.python.org/pypi/ssl_api/
    :alt: Latest version

.. image:: https://pypip.in/wheel/ssl_api/badge.png
    :target: https://pypi.python.org/pypi/ssl_api/
    :alt: Wheel Status

.. image:: https://pypip.in/license/ssl_api/badge.png
    :target: https://pypi.python.org/pypi/ssl_api/
    :alt: License


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

   Start in the foreground with debugging:

     ```
     $ ca_start_gunicorn_dev
     ```

   Start in the background without debugging, with the right user, etc..:

     ```
     CA_PASSPHRASE=test ca_start_gunicorn_prod
     ```

   A passphrase is required. If it is not found as "CA_PASSPHRASE" in the
   environment, the user will be prompted. See the section [Notes on Automatic 
   Startup](#notes-on-automatic-startup) for details.
   
6. Configure your webserver. 

   This is a simple matter of adding a website that proxies incoming requests 
   to the CA server at */tmp/ssl_api.gunicorn.sock*. The developers recommend 
   the [Nginx](http://wiki.nginx.org) web-server. 

   It is, obviously, highly recommended that your CA server is configured for 
   SSL.

   No directory need be defined in the webserver config since there is no 
   presentational logic. 

   This is an example Nginx config:

    upstream ca_app_server {
        server unix:/tmp/ssl_api.gunicorn.sock fail_timeout=0;
    }

        server {
            listen      443;
            server_name ca.company.com;
            keepalive_timeout 5;

            # These ciphers include support for PFS.
            ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
            ssl_prefer_server_ciphers on;
            ssl_ciphers EECDH+ECDSA+AESGCM:EECDH+aRSA+AESGCM:EECDH+ECDSA+SHA256:EECDH+aRSA+RC4:EDH+aRSA:EECDH:RC4:!aNULL:!eNULL:!LOW:!3DES:!MD5:!EXP:!PSK:!SRP:!DSS;

            ssl on;
            ssl_certificate     /etc/ssl/certs/company.key.pem;
            ssl_certificate_key /etc/ssl/private/company.crt.pem;

            location / {
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header Host $http_host;
                proxy_redirect off;

                proxy_pass   http://ca_app_server;
            }
        }


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

An example of how the server can be started:

```bash
source /root/.ca_passphrase
PYTHONPATH=/usr/local/lib/python2.7/dist-packages/deploy_ca
/usr/local/bin/ca_start_gunicorn_prod
```

where /root/.ca_passphrase has something like:

```
export CA_PASSPHRASE="test"
```

In this case, you'll have to make sure the passphrase file is very restricted, 
permission-wise. Absolute paths are used in the example script, above, because 
it might be called prior to the definition of an executable search path.


API Usage
---------

There is exactly one endpoint, which expects a PUT request of the CSR PEM file:

    /api/csr/[a-zA-Z0-9]+

The URL path expects a client ID/hash having alphanumeric characters but not 
symbols. This represents an identifier that will allow you to map a 
request to a particular client/customer. This will most often be used to verify 
membership or billing. If you do not require this support, then just choose 
some arbitrary value, and give that URL to everyone who might use the API (any 
potential use of this value is done only from your callbacks).

The response will be a JSON dictionary with key "signed_x509_pem" containing 
the new certificate.


Implementing Callbacks and Other Custom Configuration
-----------------------------------------------------

The default configuration of *ssl_api* defines several API callbacks that 
generally don't do anything. These configuration modules may also define 
values that you'd like to customize (such as where the CA's identity path is 
located).

At the bottom of these modules, an attempt is made to perform an import. If
custom functionality is found, the module-level variables in that module will
overwrite the module-level variables in that config file.

The following table expresses what configuration modules are used by *ssl_api*, 
the import that is attempted, and what callbacks are defined (though all 
variables in the configuration modules can be overriden).

| Config Module          | Attempted Import                 | Callbacks                                  |
| ---------------------- | -------------------------------- | ------------------------------------------ |
| sapi.config.ca         | from sapi_custom_ca.ca import *  | CUSTOM_BOOT_CB, SERIAL_NUMBER_GENERATOR_CB |
| sapi.config.api.server | from sapi_custom_ca.api import * | API_CSR_HOOKS_FACTORY                      |

### Callback Descriptions

| Callback                   | Description                                            |
| -------------------------- | ------------------------------------------------------ |
| CUSTOM_BOOT_CB             | Triggered on load. Raise a *sapi.exceptions.CsrNotAuthedError* if a certificate should not be generated. |
| SERIAL_NUMBER_GENERATOR_CB | SN generator for new certificates. Defaults to a SHA1 of the current epoch and the next value from Python's PRNG |
| API_CSR_HOOKS_FACTORY      | Generates objects that encapsulate signing a particular CSR. Must inherit from *sapi.config.api.signing_hooks_base.SigningHooksBase*. |

The "SigningHooksBase" base-class that a hooks class must inherit from defines 
the following methods to be overridden:

| Method | Description |
| ------ | ----------- |
| authorize(subject_alt_name_exts) | A request has been received. |
| presign(certificate) | A certificate has been built and is about to be signed. Is an M2Crypto.X509 object. |
| postsign(certificate) | A certificate has been signed and is about to be returned. Is an M2Crypto.X509 object. |

The base-class also exposes the following properties:

| Property | Description |
| -------- | ----------- |
| client_hash | The client-hash from the current HTTP request. |
| public_key_hash | A SHA1 (lower-case) hash of the public-key received with the CSR. | 
| csr_tuple | (&lt;PEM string&gt;, &lt;M2Crypto CSR object&gt;, &lt;PyOpenSSL CSR object&gt;) |


Other Details
--------------

- The default length of the CA key created by the ca_create_identity tool is 
  2048-bits. If you'd like a different length, just provide your own identity 
  files.


Compatibility
-------------

As this project uses web.py, it is only compatible with Python 2.x .


Unsupported functionalities
---------------------------

- We do not directly support CRLs/OCSP/etc.. for certificate revocation. If 
  desired, it'll be up to the developer to add a CDP (CRL distribution point) 
  or OCSP access URL from the pre-signing callback, and then host it 
  themselves.


Disclaimer
----------

This project (and its documentation) is currently approaching final release. As 
such it is still subject to change (probably not by much, though).
