#!/bin/bash

# Check if running root. Required to install tflite-runtime
if [ "$EUID" -ne 0 ]
  then
  echo "Please run the install script as root. It is required to install the Tensorflow lite runtime."
  exit
fi

echo "Installing required pip packages..."

echo "Installing numpy..."
pip3 install numpy

echo "Installing simple-websocket-server..."
pip3 install simple-websocket-server

echo "Installing opencv-python..."
pip3 install opencv-python

echo "Installing setuptools..."
pip3 install setuptools

echo "Installing tflite-runtime..."
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | tee /etc/apt/sources.list.d/coral-edgetpu.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
apt-get update
apt-get install python3-tflite-runtime
if [ $? -ne 0 ]
  then
  echo "ERROR! Failed to install Tensorflow Lite!"
  echo "While Tensorflow does not recommend install it through pip on Debian it is possible."
  echo "Other software using Tensorflow Lite may cause runtime failures."
  echo "Do you want to install Tensorflow Lite using pip? (y/n):"
  read -n1r cont
  if [ "$cont" != 'y' ] && [ "$cont" != 'Y' ]
    then
    echo "Installation failed. Aborting..."
    exit
  fi
  echo "Using pip to install Tensorflow Lite"
  pip3 install --extra-index-url https://google-coral.github.io/py-repo/ tflite_runtime
fi

echo "Finished installing dependencies."
echo "Installing camera-security package..."
pip3 install ./

echo "Camera Security installed. To start the server run the run.sh script."
echo "Default user password is \"pass\" (without the quotes)."
echo "Please change it after connecting with the client for the first time."
echo "You can configure the server by modifying the settings.ini file."