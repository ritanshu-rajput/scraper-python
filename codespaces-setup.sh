#!/bin/bash
# Codespaces Quick Setup Script

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║     GitHub Codespaces Setup - Planning App Scraper       ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if we're in Codespaces
if [ -n "$CODESPACES" ]; then
    echo "✓ Running in GitHub Codespaces"
else
    echo "⚠ Not detected as Codespaces, but continuing anyway..."
fi
echo ""

# Install Python packages
echo "▶ Installing Python packages..."
pip install -q -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✓ Python packages installed"
else
    echo "✗ Failed to install Python packages"
    exit 1
fi
echo ""

# Install Chromium
echo "▶ Installing Chromium browser..."
sudo apt-get update -qq
sudo apt-get install -y -qq chromium-browser chromium-chromedriver
if [ $? -eq 0 ]; then
    echo "✓ Chromium installed"
else
    echo "✗ Failed to install Chromium"
    exit 1
fi
echo ""

# Create directories
echo "▶ Setting up directories..."
mkdir -p data/pdfs output/letters output/csv templates logs
echo "✓ Directories created"
echo ""

# Create letter template
echo "▶ Creating letter template..."
python main.py create-template > /dev/null 2>&1
if [ -f "templates/letter_template.docx" ]; then
    echo "✓ Template created at templates/letter_template.docx"
else
    echo "⚠ Template creation may have failed"
fi
echo ""

# Run test
echo "▶ Running test to verify setup..."
python test_example.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ Test passed!"
else
    echo "⚠ Test may have issues, check logs"
fi
echo ""

# Show generated files
echo "═══════════════════════════════════════════════════════════"
echo "✓ Setup Complete!"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Generated test files:"
ls -lh output/csv/ 2>/dev/null | grep -v total || echo "  No files yet"
ls -lh output/letters/ 2>/dev/null | grep -v total || echo "  No files yet"
echo ""
echo "Next steps:"
echo "  1. Edit the template: templates/letter_template.docx"
echo "  2. Run the scraper: python main.py run south_lanarkshire"
echo "  3. Check results: ls output/csv/ && ls output/letters/"
echo ""
echo "Quick commands:"
echo "  python main.py list-councils    # View available councils"
echo "  python main.py run south_lanarkshire    # Run scraper"
echo "  python test_example.py          # Run test without scraping"
echo ""
echo "Documentation: See README.md and CODESPACES.md"
echo "═══════════════════════════════════════════════════════════"
