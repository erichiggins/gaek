#!/bin/bash

GAE_SDK_SHA1='02ca467d77f5681c52741c7223fb8e97dff999da'
GAE_SDK_FILE='google_appengine_1.9.50.zip'

# Create virtual environment.
echo 'Creating virtual environment...'
virtualenv .dev_env
source .dev_env/bin/activate
pip install --upgrade ndg-httpsclient
pip install --upgrade pip
pip install --upgrade nose

# Download the App Engine SDK.
echo "Downloading $GAE_SDK_FILE..."
curl -O https://storage.googleapis.com/appengine-sdks/featured/$GAE_SDK_FILE
  
echo "Verifying $GAE_SDK_FILE..."
shasum $GAE_SDK_FILE
  
echo "Unzipping $GAE_SDK_FILE..."
unzip -q $GAE_SDK_FILE -d .dev_env/
rm $GAE_SDK_FILE
cd .dev_env/lib/python2.7/site-packages/
ln -s ../../../google_appengine/google google
cd ../../../../
