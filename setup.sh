#!/bin/bash

# Activate the Python virtual environment
echo "Activating the virtual environment..."
source /home/adminuser/venv/bin/activate || { echo "Failed to activate virtual environment"; exit 1; }

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r /mount/src/face_recognition/requirements.txt || { echo "Failed to install Python dependencies"; exit 1; }

echo "Setup completed successfully!"
