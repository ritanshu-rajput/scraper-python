# Planning Application Scraper & Letter Generator

An automated Python tool that scrapes planning applications from council websites, extracts applicant details from PDFs, and generates personalized letters.

## Features

✅ **Automated Web Scraping** - Scrapes weekly planning applications from council websites
✅ **PDF Extraction** - Extracts applicant details (name, address, contact info) from application forms
✅ **Data Storage** - Saves extracted data to CSV files with timestamps
✅ **Letter Generation** - Creates personalized letters using customizable templates
✅ **Multiple Formats** - Supports DOCX and PDF output for letters
✅ **Robust Error Handling** - Comprehensive logging and retry mechanisms
✅ **Easy CLI** - Simple command-line interface for all operations

## Project Structure

```
scraper-python/
├── main.py                  # Main CLI script
├── setup.sh                 # Automated setup script
├── requirements.txt         # Python dependencies
├── README.md               # This file
│
├── config/                 # Configuration
│   ├── __init__.py
│   └── config.py           # Main configuration file
│
├── src/                    # Source code
│   ├── __init__.py
│   └── modules/
│       ├── __init__.py
│       ├── scraper.py           # Web scraping module
│       ├── pdf_extractor.py     # PDF extraction module
│       ├── csv_handler.py       # CSV operations module
│       └── letter_generator.py  # Letter generation module
│
├── data/                   # Data directory
│   └── pdfs/              # Downloaded PDF files
│
├── output/                # Output directory
│   ├── csv/              # CSV files with extracted data
│   └── letters/          # Generated letters
│
├── templates/            # Letter templates
│   └── letter_template.docx
│
└── logs/                 # Log files
    └── scraper.log
```

## Requirements

- Python 3.8 or higher
- Chrome or Chromium browser
- Internet connection

## Installation

### Option 1: Automated Setup (Recommended)

```bash
# Clone or download the project
cd scraper-python

# Run the setup script
./setup.sh
```

### Option 2: Manual Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create letter template
python main.py create-template
```

### Installing Chrome/Chromium

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install chromium-browser
```

**MacOS:**
```bash
brew install --cask google-chrome
```

**Windows:**
Download and install Chrome from: https://www.google.com/chrome/

## Usage

### 1. Create and Customize Letter Template

First, create a template file:

```bash
python main.py create-template
```

Then edit `templates/letter_template.docx` with your letter content. Use these placeholders:

- `{DATE}` - Current date
- `{APPLICANT_NAME}` - Applicant's full name
- `{APPLICANT_ADDRESS}` - Applicant's address
- `{POSTCODE}` - Applicant's postcode
- `{EMAIL}` - Applicant's email
- `{PHONE}` - Applicant's phone number
- `{APPLICATION_NUMBER}` - Planning application reference
- `{SITE_ADDRESS}` - Development site address
- `{DEVELOPMENT_DESCRIPTION}` - Description of proposed development

### 2. Run the Scraper

**Full workflow (scraping + extraction + CSV + letters):**

```bash
python main.py run south_lanarkshire
```

**Skip scraping (use existing PDFs):**

```bash
python main.py run south_lanarkshire --skip-scraping
```

**Skip letter generation:**

```bash
python main.py run south_lanarkshire --skip-letters
```

**Verbose logging:**

```bash
python main.py run south_lanarkshire --verbose
```

### 3. View Available Councils

```bash
python main.py list-councils
```

### 4. Access Results

After running, you'll find:

- **CSV Data**: `output/csv/planning_applications_YYYY-MM-DD.csv`
- **Contact List**: `output/csv/contact_list_YYYY-MM-DD.csv`
- **Letters**: `output/letters/Letter_[AppNumber]_[ApplicantName].docx`
- **PDFs**: `data/pdfs/[ApplicationReference].pdf`
- **Logs**: `logs/scraper.log`

## Command Reference

### Main Commands

| Command | Description |
|---------|-------------|
| `python main.py run <council>` | Run the full workflow |
| `python main.py create-template` | Create letter template |
| `python main.py list-councils` | List available councils |

### Options

| Option | Description |
|--------|-------------|
| `--skip-scraping` | Use existing PDFs, don't scrape |
| `--skip-letters` | Don't generate letters |
| `--verbose` | Enable detailed logging |

## Configuration

Edit `config/config.py` to customize:

### Add New Councils

```python
COUNCILS = {
    "south_lanarkshire": {
        "name": "South Lanarkshire",
        "url": "https://publicaccess.southlanarkshire.gov.uk/online-applications/search.do?action=weeklyList",
        "enabled": True
    },
    # Add more councils here
    "your_council": {
        "name": "Your Council Name",
        "url": "https://...",
        "enabled": True
    }
}
```

### Scraper Settings

```python
SCRAPER_CONFIG = {
    "headless": True,           # Run browser in background
    "timeout": 30,              # Page load timeout
    "download_delay": 2,        # Delay between downloads
    "max_retries": 3           # Retry attempts
}
```

### Letter Settings

```python
LETTER_CONFIG = {
    "template_file": "letter_template.docx",
    "output_format": "docx",    # 'docx' or 'pdf'
    "font_name": "Arial",
    "font_size": 11
}
```

## Troubleshooting

### Chrome/ChromeDriver Issues

**Error: "chromedriver not found"**

The scraper should automatically download ChromeDriver. If issues persist:

```bash
pip install webdriver-manager --upgrade
```

**Error: "Chrome version mismatch"**

Update Chrome to the latest version or run:

```bash
pip install selenium --upgrade
```

### PDF Extraction Issues

**Error: "Failed to extract text from PDF"**

Some PDFs may be scanned images. The scraper tries multiple extraction methods, but OCR is not included. Consider:

1. Manually checking problematic PDFs
2. Using commercial OCR tools for scanned documents

### No Applications Found

**Check these:**

1. Website is accessible and structure hasn't changed
2. Your IP isn't blocked (try manually accessing the site)
3. Check logs at `logs/scraper.log` for detailed errors

### Letter Generation Issues

**Error: "Template not found"**

```bash
python main.py create-template
```

**PDF Conversion Issues**

PDF conversion requires LibreOffice or docx2pdf. On Linux:

```bash
sudo apt-get install libreoffice
```

## Scheduled Automation

### Linux/Mac (cron)

Run weekly on Monday at 9 AM:

```bash
# Edit crontab
crontab -e

# Add this line:
0 9 * * 1 cd /path/to/scraper-python && /path/to/scraper-python/venv/bin/python main.py run south_lanarkshire
```

### Windows (Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (weekly, Monday, 9 AM)
4. Action: Start a program
5. Program: `C:\path\to\scraper-python\venv\Scripts\python.exe`
6. Arguments: `main.py run south_lanarkshire`
7. Start in: `C:\path\to\scraper-python`

## Advanced Usage

### Using Existing PDFs

If you already have PDFs downloaded:

1. Place them in `data/pdfs/`
2. Run: `python main.py run south_lanarkshire --skip-scraping`

### Batch Processing Multiple Councils

```bash
#!/bin/bash
for council in south_lanarkshire north_lanarkshire east_ayrshire; do
    python main.py run $council
    sleep 60  # Wait 60 seconds between councils
done
```

### Exporting to Google Sheets

The CSV files can be imported to Google Sheets:

1. Open Google Sheets
2. File → Import → Upload
3. Select the CSV file from `output/csv/`

### Airtable Integration

Use Airtable's CSV import feature:

1. Create Airtable base
2. Import CSV from `output/csv/`
3. Set up automation with Airtable API if needed

## Data Privacy & Legal

⚠️ **Important Notes:**

- Planning applications are public records
- Ensure compliance with GDPR and local data protection laws
- Use extracted data responsibly and lawfully
- Only use for legitimate business purposes
- Respect council website terms of service
- Consider rate limiting and being respectful to servers

## Support & Maintenance

### Logs

Check logs for errors:
```bash
tail -f logs/scraper.log
```

### Common Issues

Most issues are logged. Check the log file for detailed error messages and stack traces.

### Updating

To update dependencies:
```bash
pip install -r requirements.txt --upgrade
```

## Development

### Project Dependencies

- **selenium**: Web browser automation
- **beautifulsoup4**: HTML parsing
- **PyPDF2 & pdfplumber**: PDF text extraction
- **python-docx**: Word document generation
- **requests**: HTTP requests

### Adding Features

The modular structure makes it easy to extend:

- `src/modules/scraper.py`: Modify scraping logic
- `src/modules/pdf_extractor.py`: Enhance PDF extraction patterns
- `src/modules/letter_generator.py`: Customize letter formatting
- `config/config.py`: Add new councils or change settings

## Example Output

### CSV Output

```csv
application_number,applicant_name,applicant_address,email,phone
P/23/1234,John Smith,123 Main Street,john@email.com,01234567890
P/23/1235,Jane Doe,456 Oak Avenue,jane@email.com,01234567891
```

### Generated Letters

Letters are saved as:
- `Letter_P_23_1234_John_Smith.docx`
- `Letter_P_23_1235_Jane_Doe.docx`

## License

This project is provided as-is for legitimate business use. Ensure compliance with all applicable laws and regulations.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## Version History

- **v1.0.0** - Initial release with core functionality

---

**Made with ❤️ for automating planning application workflows**
