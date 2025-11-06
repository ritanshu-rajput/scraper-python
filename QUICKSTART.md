# Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites

- Python 3.8+
- Chrome or Chromium browser
- Internet connection

## Installation

### Linux/Mac

```bash
# 1. Navigate to project directory
cd scraper-python

# 2. Run setup script
./setup.sh

# 3. Activate virtual environment
source venv/bin/activate
```

### Windows

```bash
# 1. Navigate to project directory
cd scraper-python

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create template
python main.py create-template
```

## Quick Test

Run a test to verify everything works:

```bash
python test_example.py
```

You should see:
- ✓ CSV files created in `output/csv/`
- ✓ Letters generated in `output/letters/`

## First Run

### Step 1: Customize Your Letter Template

```bash
# Open and edit the template
# Linux/Mac
open templates/letter_template.docx

# Windows
start templates\letter_template.docx
```

Edit the template with your company information and letter content.

### Step 2: Run the Scraper

```bash
# Full workflow: scrape → extract → save → generate letters
python main.py run south_lanarkshire
```

**Note:** The first run may take longer as it downloads ChromeDriver.

### Step 3: Check Your Results

```bash
# View generated files
ls output/csv/        # CSV files
ls output/letters/    # Generated letters
ls logs/             # Log files
```

## Common Commands

```bash
# List available councils
python main.py list-councils

# Run with verbose logging
python main.py run south_lanarkshire --verbose

# Skip scraping (use existing PDFs)
python main.py run south_lanarkshire --skip-scraping

# Skip letter generation
python main.py run south_lanarkshire --skip-letters

# View help
python main.py --help
```

## Troubleshooting

### "Chrome not found"

Install Chrome or Chromium:

```bash
# Ubuntu/Debian
sudo apt-get install chromium-browser

# MacOS
brew install --cask google-chrome
```

### "Module not found"

Make sure you activated the virtual environment:

```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### "Permission denied" on setup.sh

```bash
chmod +x setup.sh
./setup.sh
```

## Next Steps

1. Read [README.md](README.md) for detailed documentation
2. Customize `config/config.py` for your needs
3. Add more councils to the configuration
4. Set up scheduled automation (see README.md)

## Getting Help

- Check `logs/scraper.log` for detailed error messages
- Review [README.md](README.md) for comprehensive documentation
- Run with `--verbose` flag for detailed output

## Example Workflow

```bash
# 1. Activate environment
source venv/bin/activate

# 2. Run scraper (weekly task)
python main.py run south_lanarkshire

# 3. Check results
cat output/csv/planning_applications_$(date +%Y-%m-%d).csv

# 4. View letters
ls -l output/letters/

# Done! 🎉
```

## Scheduled Weekly Run

Add to crontab for weekly automation:

```bash
# Run every Monday at 9 AM
0 9 * * 1 cd /path/to/scraper-python && ./venv/bin/python main.py run south_lanarkshire
```

---

**Ready to go! 🚀** For detailed documentation, see [README.md](README.md)
