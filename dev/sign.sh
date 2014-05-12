#!/bin/sh

if [ "$1" == "" ]; then
    echo "No CSR provided."
    exit 1
fi

PYTHONPATH=../resources/custom_example ../scripts/sign_subordinate -f $1 1y
