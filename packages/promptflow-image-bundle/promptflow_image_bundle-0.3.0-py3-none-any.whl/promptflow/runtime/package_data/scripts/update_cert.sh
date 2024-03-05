#!/bin/bash

# In AirGapped Cloud, we need to update and trust special CA certs from wireserver to connect to Azure.
# For other clouds, no need to change.
CLOUD_NAME=${AML_CloudName:-"AzureCloud"}
if [[ $CLOUD_NAME == "USSec" || $CLOUD_NAME == "USNat" ]]; then
    echo "Updating certificate for $CLOUD_NAME"
    # copy certificates from host to container, and install
    HOST_AZURE_CERT_DIR="/mnt/host/root/AzureCACertificates"
    LOCAL_AZURE_CERT_DIR="/usr/local/share/ca-certificates/azure"
    mkdir -p $LOCAL_AZURE_CERT_DIR
    cp -r $HOST_AZURE_CERT_DIR/* $LOCAL_AZURE_CERT_DIR
    update-ca-certificates

    # set environment variables to use installed custom CA bundle, e.g. for Python requests
    export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
    export SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
fi
