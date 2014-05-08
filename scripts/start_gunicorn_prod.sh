#!/bin/sh

cd ..

PYTHONPATH=. gunicorn -c resources/gunicorn.conf.prod sapi.wsgi:wsgi
