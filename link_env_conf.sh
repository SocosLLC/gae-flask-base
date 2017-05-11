#!/usr/bin/env bash

if [ -z $1 ]; then
    echo "Usage: $0 ENV_CONF_EXTENSION"
    exit 1
fi

FULL_PATH=src/application/config/env_conf.py.$1
if [ ! -e $FULL_PATH ]; then
    echo "No such env conf: $FULL_PATH"
    exit 1
fi

cd src/application ;

# Remove compiled version
if [ -e env_conf.pyc ]; then
    rm env_conf.pyc
fi

ln -sf config/env_conf.py.$1 env_conf.py ;
cd ../..
