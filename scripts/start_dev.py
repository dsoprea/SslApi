#!/usr/bin/env python2.7

from sys import path
path.insert(0, '.')

from os import chdir
chdir('..')

import logging

import sapi.app.main
import sapi.ssl.ca

# Induce the CA passphrase to be asked and remembered.
sapi.ssl.ca.ca_factory()

# Configure logging.

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.WARNING)
logging.getLogger('jenkinsapi.job').setLevel(logging.WARNING)

sapi.app.main.app.run()
