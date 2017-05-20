#!/usr/bin/env bash

echo
echo "Installing npm dependencies"
echo "---------------------------"
# postcss/autoprefixer for compiling assets. See src/assets.py
if ! hash postcss 2>/dev/null; then
    sudo npm -g install postcss-cli autoprefixer
fi
# bower for asset management
if ! hash bower 2>/dev/null; then
    sudo npm install -g bower
fi
# phantomjs for Selenium tests
if ! hash phantomjs 2>/dev/null; then
    sudo npm install -g phantomjs-prebuilt
fi

echo
echo "Setting up virtualenv"
echo "---------------------"
virtualenv env
./env/bin/easy_install -U pip
./env/bin/pip install --upgrade -r requirements.txt
source env/bin/activate

echo
echo "Creating symlinks"
echo "-----------------"
if [ ! -L src/libs ]; then
    cd src/
    ln -s ../env libs
    cd ..
fi

echo
echo "Running bower install"
echo "---------------------"
bower install

if [ ! -f src/application/secret_keys.py ]; then
    cd src/
    ./generate_keys.py
    cd ../
fi

echo
echo "Building assets"
echo "---------------"
./src/assets.py

deactivate

