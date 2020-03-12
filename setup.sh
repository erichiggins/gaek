#!/bin/bash

GAE_SDK_SHA1='35c6857852f787ab777824ceaf645964cff696bc'
GAE_SDK_FILE='google_appengine_1.9.88.zip'

# Create virtual environment.
echo 'Creating virtual environment...'
virtualenv .dev_env
source .dev_env/bin/activate
pip install --upgrade ndg-httpsclient
pip install --upgrade pip

# Download the App Engine SDK.
echo "Downloading $GAE_SDK_FILE..."
curl -O https://storage.googleapis.com/appengine-sdks/featured/$GAE_SDK_FILE
  
echo "Verifying $GAE_SDK_FILE..."
shasum $GAE_SDK_FILE

echo "Unzipping $GAE_SDK_FILE..."
unzip -q $GAE_SDK_FILE -d .dev_env/
rm $GAE_SDK_FILE

# Travis CI uses a different path.
if [ -d ".dev_env/site-packages/" ]; then
  cd .dev_env/site-packages/
  ln -s ../google_appengine/google google
fi

# OSX path.
if [ -d ".dev_env/lib/python2.7/site-packages/" ]; then
  cd .dev_env/lib/python2.7/site-packages/
  ln -s ../../../google_appengine/google google
  cd ../../../../
fi
