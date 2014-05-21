#!/bin/sh

if [ "$1" == "" ]; then
    echo "No CSR provided."
    exit 1
fi

PYTHONPATH=../sapi/resources/custom_example ../scripts/ca_sign_subordinate -f $1 1y
