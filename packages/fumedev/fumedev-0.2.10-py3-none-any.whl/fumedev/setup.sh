#!/usr/bin/env bash
# The script's own path
SELF=$(realpath "$0")

REPO_URL="git@github.com:FumeDev/fume_python_server_mac_os_arm.git"
BASE_DIR="FumeDev" 


DIR_PATH="$HOME/$BASE_DIR"

if [ -d "$DIR_PATH" ]; then

    echo "Directory exists. Pulling latest changes..."
    cd "$DIR_PATH"
    git fetch --all
    git reset --hard origin/main

else
   
    echo "Directory does not exist. Cloning repository..."
    git clone "$REPO_URL" "$DIR_PATH"
fi


# Check if the DIR_PATH is defined
if [ -z "$DIR_PATH" ]; then
    echo "DIR_PATH is not set. Please set it before running the script."
    exit 1
fi

# Check if the .env file exists in DIR_PATH
env_file="$DIR_PATH/.env"
if [ ! -f "$env_file" ]; then
    # If the .env file does not exist, create it
    echo "Creating .env file in $DIR_PATH..."
    touch "$env_file"
fi

# Loop through each environment variable and add/append it
for env_var in "${ENV_VARS[@]}"; do
    add_env_var "$env_var"
done

# Destination directory
DEST="/usr/local/bin/FumeDev"

if [ ! -e "$DEST" ]; then
    # Check for root privileges
    if [ "$(id -u)" != "0" ]; then
        echo "This script must be run as root" >&2
        exit 1
    fi

    # Copy the script to the global path
    cp "$SELF" "$DEST"

    # Make the script executable
    chmod +x "$DEST"

    echo "Script copied to $DEST"

else
    pip3 install -r requirements.txt
    echo "Starting Python server..."
    python3 start.py
fi

