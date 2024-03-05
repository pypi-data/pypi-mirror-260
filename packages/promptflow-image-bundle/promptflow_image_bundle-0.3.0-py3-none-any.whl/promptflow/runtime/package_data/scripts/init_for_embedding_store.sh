#! /bin/bash

# these environment variables are used by embedding store
export EMBEDDING_STORE_LOCAL_CACHE_PATH="/service/embedding-store/"
export EMBEDDING_STORE_SERVICE_HOST="http://localhost"
export EMBEDDING_STORE_SERVICE_PORT="23333"
export IS_EMBEDDING_STORE_REST_SERVICE_ENABLED="false"

if [ ! -d ${EMBEDDING_STORE_LOCAL_CACHE_PATH} ]; then
    mkdir -p ${EMBEDDING_STORE_LOCAL_CACHE_PATH}
fi
