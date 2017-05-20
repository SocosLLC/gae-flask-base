#!/bin/sh

TESTARGS=${@:-"src/tests/"}

set +e  # Don't die before we clean up
./link_env_conf.sh test
mkdir -p tmp/
./env/bin/python src/assets.py
./env/bin/nosetests \
                    --with-gae \
                    --verbose \
                    --gae-application src/ \
                    ${TESTARGS}
RETVAL=$?
./link_env_conf.sh dev

exit ${RETVAL}
