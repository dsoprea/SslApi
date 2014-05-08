#!/bin/sh

cd ..

PYTHONPATH=. gunicorn -c resources/gunicorn.conf.dev sapi.wsgi:wsgi
