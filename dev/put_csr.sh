#!/bin/sh

curl -X POST --data-binary @$HOME/testServer.csr -H "Content-Type: application/x-pem-file" http://localhost:8080/api/csr
