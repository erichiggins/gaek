#!/bin/bash

GAE_SDK_SHA1='35c6857852f787ab777824ceaf645964cff696bc'
GAE_SDK_FILE='google_appengine_1.9.88.zip'
SITE_PKGS="$(python -c 'import sys; print(sys.path[-1])')"
ENV_PATH="$(pwd)/.dev_env"

# Create virtual environment outside of CI.
if [[ -z "${CONTINUOUS_INTEGRATION}" ]]; then
  echo 'Creating virtual environment...'
  virtualenv $ENV_PATH
  source $ENV_PATH/bin/activate
  SITE_PKGS="$(python -c 'import sys; print(sys.path[-1])')"
else
  ENV_PATH="~/virtualenv/python$TRAVIS_PYTHON_VERSION"
fi

pip install --upgrade ndg-httpsclient
pip install --upgrade pip

# Download the App Engine SDK.
echo "Downloading $GAE_SDK_FILE..."
curl -O https://storage.googleapis.com/appengine-sdks/featured/$GAE_SDK_FILE
  
echo "Verifying $GAE_SDK_FILE..."
shasum $GAE_SDK_FILE

echo "Unzipping $GAE_SDK_FILE..."
unzip -q $GAE_SDK_FILE -d $ENV_PATH/
rm $GAE_SDK_FILE

# Symlink the google directory to add it to site-packages
echo "Creating symlink to google path..."
cd $SITE_PKGS
pwd
ln -s $ENV_PATH/google_appengine/google google
