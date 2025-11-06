#!/bin/bash
# Setup script for Planning Application Scraper

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║     Planning Application Scraper - Setup Script          ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "▶ Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "✗ Error: Python 3 is not installed"
    exit 1
fi

echo "✓ Python 3 is installed"
echo ""

# Create virtual environment
echo "▶ Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "✗ Error: Failed to create virtual environment"
    exit 1
fi

echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "▶ Activating virtual environment..."
source venv/bin/activate

echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "▶ Upgrading pip..."
pip install --upgrade pip

echo ""

# Install requirements
echo "▶ Installing required packages..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "✗ Error: Failed to install requirements"
    exit 1
fi

echo "✓ All packages installed successfully"
echo ""

# Check for Chrome/Chromium
echo "▶ Checking for Chrome/Chromium..."
if command -v google-chrome &> /dev/null; then
    echo "✓ Google Chrome found"
elif command -v chromium-browser &> /dev/null; then
    echo "✓ Chromium found"
elif command -v chromium &> /dev/null; then
    echo "✓ Chromium found"
else
    echo "⚠ Warning: Chrome/Chromium not found"
    echo "  Please install Chrome or Chromium for the scraper to work"
    echo "  Ubuntu/Debian: sudo apt-get install chromium-browser"
    echo "  MacOS: brew install --cask google-chrome"
fi

echo ""

# Create necessary directories
echo "▶ Setting up directories..."
mkdir -p data/pdfs output/letters output/csv templates logs

echo "✓ Directories created"
echo ""

# Create sample template
echo "▶ Creating sample letter template..."
python main.py create-template

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                   Setup Complete!                         ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Edit the letter template: templates/letter_template.docx"
echo "  3. Run the scraper: python main.py run south_lanarkshire"
echo ""
echo "For more information, see README.md"
echo ""
