#!/bin/bash

ORIGINAL_DIR=$(pwd)
# Dynamically get the user's home directory
USER_HOME=$(eval echo ~$USER)

# Path to your Python program
PROGRAM_DIR="./"
cd $PROGRAM_DIR

# Check if the program path exists
if [ -f "start.py" ]; then
    # Run your Python program
    python3 "start.py" "$ORIGINAL_DIR" "$@"
else
    echo "Error: Python program not found at $PROGRAM_PATH"
    exit 1
fi