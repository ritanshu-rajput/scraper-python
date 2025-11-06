# Running in GitHub Codespaces

This guide shows you how to run the Planning Application Scraper in GitHub Codespaces.

## Quick Start (1 minute)

### 1. Open in Codespaces

```bash
# You're already in Codespaces if you see this file!
# Otherwise, click the green "Code" button → "Codespaces" → "Create codespace on main"
```

### 2. Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Install Chromium (required for web scraping)
sudo apt-get update
sudo apt-get install -y chromium-browser chromium-chromedriver
```

### 3. Run a Test

```bash
# Test that everything works
python test_example.py
```

You should see:
```
✓ CSV files created in output/csv/
✓ Letters generated in output/letters/
```

### 4. Create Letter Template

```bash
python main.py create-template
```

Then edit `templates/letter_template.docx` with your content.

### 5. Run the Scraper

```bash
# Full workflow
python main.py run south_lanarkshire
```

---

## One-Line Setup (Copy & Paste)

```bash
pip install -q -r requirements.txt && sudo apt-get update -qq && sudo apt-get install -y -qq chromium-browser chromium-chromedriver && python test_example.py
```

---

## What This Does in Codespaces

1. **Installs Python packages** - All required libraries
2. **Installs Chromium browser** - Needed for web scraping
3. **Runs a test** - Verifies everything works
4. **Generates sample outputs** - CSV files and letters

---

## Common Codespaces Commands

```bash
# View generated CSV files
cat output/csv/test_applications.csv

# List generated letters
ls -lh output/letters/

# View logs
tail -f logs/scraper.log

# Run with verbose output
python main.py run south_lanarkshire --verbose

# Test without scraping (uses test data)
python test_example.py
```

---

## Codespaces-Specific Notes

### Browser Configuration

In Codespaces, the scraper runs in **headless mode** (no visible browser window), which is perfect for cloud environments.

### File Access

- **Download files**: Right-click any file in VS Code explorer → Download
- **View CSV**: Click any CSV file to view in VS Code
- **Edit template**: Click `templates/letter_template.docx` (requires extension)

### Port Forwarding

No ports needed for this application - everything runs locally!

---

## Troubleshooting in Codespaces

### "Chrome not found"

```bash
sudo apt-get update
sudo apt-get install -y chromium-browser chromium-chromedriver
```

### "Permission denied"

```bash
chmod +x main.py setup.sh
```

### "Module not found"

```bash
pip install -r requirements.txt
```

---

## Step-by-Step Visual Guide

### Option 1: Quick Test (No Scraping)

```bash
# 1. Install packages
pip install -r requirements.txt

# 2. Run test
python test_example.py

# 3. Check outputs
ls output/csv/
ls output/letters/
```

### Option 2: Full Scraping

```bash
# 1. Install everything
pip install -r requirements.txt
sudo apt-get update && sudo apt-get install -y chromium-browser

# 2. Create template
python main.py create-template

# 3. Edit template (optional)
# Edit templates/letter_template.docx in VS Code

# 4. Run scraper
python main.py run south_lanarkshire

# 5. Check results
cat output/csv/planning_applications_*.csv
ls output/letters/
```

---

## Environment Variables (Optional)

You can customize settings without editing code:

```bash
# Set headless mode (already default in Codespaces)
export SCRAPER_HEADLESS=true

# Run
python main.py run south_lanarkshire
```

---

## Viewing Results in Codespaces

### CSV Files

```bash
# View in terminal
cat output/csv/test_applications.csv

# Or click the file in VS Code Explorer to view
```

### DOCX Letters

Download the `.docx` files:
1. Right-click file in Explorer
2. Click "Download"
3. Open in Word/LibreOffice on your local machine

### Logs

```bash
# View logs
cat logs/scraper.log

# Follow logs in real-time
tail -f logs/scraper.log
```

---

## Automated Setup Script

For the easiest setup:

```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Create virtual environment
- Install all packages
- Create template
- Set up directories

---

## Working with Multiple Councils

```bash
# List available councils
python main.py list-councils

# Run for specific council
python main.py run south_lanarkshire
```

---

## Tips for Codespaces

1. **Save your work**: Codespaces auto-save, but commit to git to keep changes
2. **Download outputs**: Right-click → Download for CSV/DOCX files
3. **Use terminal**: All commands work in the integrated terminal
4. **Extensions**: Install "Office Viewer" for viewing DOCX in VS Code

---

## Complete Example Session

```bash
# Step 1: Setup (one time only)
pip install -r requirements.txt
sudo apt-get update && sudo apt-get install -y chromium-browser

# Step 2: Create template (one time only)
python main.py create-template

# Step 3: Run scraper (weekly)
python main.py run south_lanarkshire

# Step 4: View results
echo "=== Applications Found ==="
wc -l output/csv/planning_applications_*.csv
echo ""
echo "=== Letters Generated ==="
ls -1 output/letters/ | wc -l
```

---

## Performance in Codespaces

- **Speed**: Similar to local machine
- **Memory**: 4GB+ available
- **Storage**: Plenty for PDFs and outputs
- **Network**: Fast downloads from council websites

---

## Keeping Codespaces Running

Codespaces auto-sleep after 30 minutes of inactivity. For long-running scrapes:

```bash
# Keep alive with periodic output
python main.py run south_lanarkshire --verbose
```

---

## Exporting Data from Codespaces

### Method 1: Download Files
Right-click → Download in VS Code

### Method 2: Git Commit
```bash
git add output/csv/*.csv
git commit -m "Weekly scrape results"
git push
```

### Method 3: Copy to Clipboard
```bash
cat output/csv/test_applications.csv | pbcopy  # Mac
cat output/csv/test_applications.csv | xclip   # Linux
```

---

## FAQ

**Q: Do I need to install Chrome?**
A: Yes, but use `chromium-browser` in Codespaces (lighter weight)

**Q: Can I run this weekly in Codespaces?**
A: Yes! Use GitHub Actions or manually open Codespace weekly

**Q: Where are my files saved?**
A: In the workspace. Commit to git or download to keep them

**Q: Can I edit the DOCX template in Codespaces?**
A: View only in Codespaces. Download to edit in Word, then re-upload

---

## Next Steps

1. ✅ Run the test: `python test_example.py`
2. ✅ Customize template: Edit `templates/letter_template.docx`
3. ✅ Run scraper: `python main.py run south_lanarkshire`
4. ✅ Download results: Right-click files → Download

---

**You're ready to go! 🚀**

Start with: `python test_example.py`
