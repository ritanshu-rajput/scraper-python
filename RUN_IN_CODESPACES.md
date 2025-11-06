# 🚀 Quick Run in GitHub Codespaces

## One-Line Setup & Test

Just copy and paste this into the Codespaces terminal:

```bash
bash codespaces-setup.sh
```

That's it! This will:
- ✅ Install all Python packages
- ✅ Install Chromium browser
- ✅ Create directories
- ✅ Create letter template
- ✅ Run a test to verify everything works

---

## Even Faster (Copy & Paste)

```bash
pip install -q -r requirements.txt && sudo apt-get update -qq && sudo apt-get install -y -qq chromium-browser && python test_example.py
```

---

## What to Do Next

### 1. **View Test Results**
```bash
# Check CSV files
cat output/csv/test_applications.csv

# List generated letters
ls -lh output/letters/
```

### 2. **Customize Letter Template**
```bash
# The template is here:
# templates/letter_template.docx
# Download it, edit in Word, then re-upload
```

### 3. **Run the Scraper**
```bash
# Full workflow
python main.py run south_lanarkshire
```

### 4. **Check Real Results**
```bash
# View today's results
cat output/csv/planning_applications_$(date +%Y-%m-%d).csv

# List all letters
ls output/letters/
```

---

## Quick Commands Reference

| Command | What It Does |
|---------|--------------|
| `python main.py run south_lanarkshire` | Run the scraper |
| `python test_example.py` | Test without scraping |
| `python main.py list-councils` | Show available councils |
| `python main.py create-template` | Create letter template |
| `cat logs/scraper.log` | View logs |

---

## Common Tasks in Codespaces

### Download Results

**Method 1: Via VS Code**
- Right-click any file in Explorer
- Click "Download"

**Method 2: Via Terminal**
```bash
# View in terminal
cat output/csv/planning_applications_*.csv
```

### Upload Custom Template

1. Edit template on your local machine
2. Drag & drop to `templates/` folder in VS Code
3. Run scraper

---

## Troubleshooting

### "Chrome not found"
```bash
sudo apt-get install -y chromium-browser chromium-chromedriver
```

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Permission denied"
```bash
chmod +x main.py codespaces-setup.sh
```

---

## Example Complete Workflow

```bash
# 1. Setup (first time only)
bash codespaces-setup.sh

# 2. Run scraper
python main.py run south_lanarkshire

# 3. View results
echo "Applications found:"
wc -l output/csv/planning_applications_*.csv

echo "Letters generated:"
ls -1 output/letters/ | wc -l

# 4. Download your files
# Right-click in VS Code → Download
```

---

## Performance Tips

- **Headless mode**: Already enabled by default (perfect for Codespaces)
- **Memory**: 4GB available, plenty for this scraper
- **Storage**: No issues with PDFs and outputs
- **Speed**: Similar to running locally

---

## Keeping Your Work

### Option 1: Commit to Git
```bash
git add output/csv/*.csv
git commit -m "Weekly scrape results"
git push
```

### Option 2: Download Files
Right-click in VS Code → Download

### Option 3: View in Terminal
```bash
cat output/csv/planning_applications_*.csv
```

---

## Full Documentation

- **Quick Start**: See [CODESPACES.md](CODESPACES.md)
- **Complete Guide**: See [README.md](README.md)
- **Quick Reference**: See [QUICKSTART.md](QUICKSTART.md)

---

## Ready to Start?

### Absolute Fastest Way:

```bash
bash codespaces-setup.sh && python main.py run south_lanarkshire
```

This will:
1. Set everything up
2. Run the scraper
3. Generate all outputs

**Time required**: ~5 minutes (depending on number of applications)

---

## Need Help?

1. Check logs: `cat logs/scraper.log`
2. Run test: `python test_example.py`
3. View help: `python main.py --help`
4. Read docs: [CODESPACES.md](CODESPACES.md)

---

**You're ready to go! 🎉**

Start with: `bash codespaces-setup.sh`
