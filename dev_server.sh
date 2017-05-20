#!/usr/bin/env bash

# Failures
function usage {
    echo "Usage:"
    echo "./dev_server.sh start|reset|kill|clean [datastore_path] [storage_path]"
    echo "    start: starts dev_appserver.py"
    echo "    kill: stops all dev_appserver.py processes using \`kill -9\`"
    echo "    reset: equivalent to \`dev_server.sh kill; dev_server.sh start\`"
    echo "    clean: deletes all the data in tmp/dev_server_storage and tmp/dev_server_datastore,"
    echo "        or <datastore_path> and <storage_path> if they are provided."
    echo "dev_appserver_args are args passed directly to dev_appserver.py"
    echo "Server runs on port 8080 and logs to tmp/dev_server.log."
    echo "Logs are not preserved between runs."
    exit 1
}

if [ $# -eq 0 ]; then
    usage
fi

if [ $1 != 'start' ] && [ $1 != 'reset' ] && [ $1 != 'kill' ] && [ $1 != 'clean' ]; then
    usage
fi

trap 'kill_ps' SIGINT SIGTERM EXIT

function rebuild {
    assets_dir="src/application/assets"
    search_dirs="${assets_dir}/src/js ${assets_dir}/src/css"
    build_file="src/assets.py"
    command="./env/bin/python ${build_file}"
    ./env/bin/when-changed ${search_dirs} -c ${command} &
}

function kill_ps {
    SERVER_PROCESS=$(ps aux | grep dev_appserver.py | grep -v grep | awk '{print $2}')
    if [[ ${SERVER_PROCESS} ]]; then
        echo "Killing server process ${SERVER_PROCESS}"
        kill -9 ${SERVER_PROCESS}
    fi
    ASSETS_PROCESS=$(ps aux | grep env/bin/when-changed | grep -v grep | awk '{print $2}')
    if [[ ${ASSETS_PROCESS} ]]; then
        echo "Killing asset reloader process ${ASSETS_PROCESS}"
        kill -9 ${ASSETS_PROCESS}
    fi
}

if [ "$1" = 'kill' ]; then
    kill_ps
    exit 0
elif [ "$1" = 'start' ]; then
    DATASTORE_PATH=${2:-"tmp/dev_server_datastore"}
    STORAGE_PATH=${3:-"tmp/dev_server_storage"}
    ./link_env_conf.sh dev
    LOG_FILE="tmp/dev_server.log"
    mkdir -p $(dirname ${DATASTORE_PATH})
    mkdir -p ${STORAGE_PATH}
    mkdir -p $(dirname ${LOG_FILE})
    rebuild &
    # It would be great to call dev_appserver.py with --quiet to bypass
    # interactive prompts, but as of 2016-12-10 it doesn't work.
    dev_appserver.py \
        --application='socos-quickstep-601' \
        --datastore_path=${DATASTORE_PATH} \
        --storage_path=${STORAGE_PATH} \
        --skip_sdk_update_check=1 \
         src/ \
         | tee ${LOG_FILE}
elif [ "$1" = 'reset' ]; then
    ./dev_server.sh kill
    ./dev_server.sh start $3 $4
elif [ "$1" = 'clean' ]; then
    DATASTORE_PATH=${2:-"tmp/dev_server_datastore"}
    STORAGE_PATH=${3:-"tmp/dev_server_storage"}
    rm -r ${STORAGE_PATH}
    rm ${DATASTORE_PATH}
fi
