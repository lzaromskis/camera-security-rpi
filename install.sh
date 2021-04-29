#!/bin/bash

# Check if running root. Required to install tflite-runtime
if [ "$EUID" -ne 0 ]
  then
    echo "Please run the install script as root. It is required to install the Tensorflow lite runtime."
    exit
fi

echo "Installing required pip packages..."

pip3 install numpy
pip3 install simple-websocket-server
pip3 install opencv-python

tee /etc/apt/sources.list.d/coral-edgetpu.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
apt-get update
apt-get install python3-tflite-runtime

echo "Finished installing dependencies."
echo "Installing camera-security package..."
pip3 install ./

echo "Camera Security installed. To start the server run the run.sh script."
echo "Default user password is \"pass\" (without the quotes)."
echo "Please change it after connecting with the client for the first time."
echo "You can configure the server by modifying the settings.ini file."