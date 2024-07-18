#!/bin/bash

# Path to the Python script
PYTHON_SCRIPT="tshark/main.py"
chmod +x "$PYTHON_SCRIPT"
while true; do
    python3 "$PYTHON_SCRIPT"
    sleep 300
done
