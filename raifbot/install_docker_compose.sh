#!/bin/bash

# Check if Docker Compose is already installed
if command -v docker-compose &> /dev/null
then
    echo "Docker Compose is already installed."
else
    echo "Docker Compose is not installed. Installing now."

    # Update the package list
    sudo apt-get update

    # Install Docker if it's not installed
    if ! command -v docker &> /dev/null
    then
        echo "Installing Docker..."
        sudo apt-get install -y docker.io
        sudo systemctl start docker
        sudo systemctl enable docker
        sudo usermod -aG docker ${USER}
    fi

    # Install Docker Compose
    echo "Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Verify the installation
echo "Docker Version:"
docker --version
echo "Docker Compose Version:"
docker-compose --version
