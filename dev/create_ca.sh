#!/bin/sh

PYTHONPATH=../sapi/resources/custom_example ../scripts/create_ca_identity -f O TestCA -f C US -f L Boynton -f ST Florida -f CN dustin.ca
