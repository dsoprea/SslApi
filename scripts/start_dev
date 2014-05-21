#!/usr/bin/env python2.7

import sys
import os.path

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, root_path)

import os
os.chdir(root_path)

#import sapi.config.log
import sapi.app.main
import sapi.ssl.ca

# Induce the CA passphrase to be asked and remembered.
sapi.ssl.ca.ca_factory()

def start():
    sapi.app.main.app.run()

if __name__ == '__main__':
    start()
