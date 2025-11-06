#!/bin/bash
# Devcontainer automatic setup script

echo "Setting up Planning Application Scraper in Codespaces..."

# Install Python requirements
pip install -q -r requirements.txt

# Install Chromium
sudo apt-get update -qq > /dev/null 2>&1
sudo apt-get install -y -qq chromium-browser chromium-chromedriver > /dev/null 2>&1

# Create directories
mkdir -p data/pdfs output/letters output/csv templates logs

# Make scripts executable
chmod +x main.py setup.sh codespaces-setup.sh

echo "✓ Setup complete! Run 'python main.py --help' to get started."
