"""
Configuration settings for Planning Application Scraper
"""
import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
TEMPLATES_DIR = BASE_DIR / "templates"
LOGS_DIR = BASE_DIR / "logs"

# Sub-directories
PDF_DIR = DATA_DIR / "pdfs"
LETTERS_DIR = OUTPUT_DIR / "letters"
CSV_DIR = OUTPUT_DIR / "csv"

# Ensure directories exist
for directory in [DATA_DIR, OUTPUT_DIR, TEMPLATES_DIR, LOGS_DIR, PDF_DIR, LETTERS_DIR, CSV_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Council configurations
COUNCILS = {
    "south_lanarkshire": {
        "name": "South Lanarkshire",
        "url": "https://publicaccess.southlanarkshire.gov.uk/online-applications/search.do?action=weeklyList",
        "enabled": True
    }
    # Add more councils here following the same format
}

# Scraper settings
SCRAPER_CONFIG = {
    "headless": True,  # Run browser in headless mode
    "timeout": 30,  # Page load timeout in seconds
    "download_delay": 2,  # Delay between downloads in seconds
    "max_retries": 3,  # Maximum number of retries for failed requests
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# PDF extraction settings
PDF_CONFIG = {
    "fields_to_extract": [
        "applicant_name",
        "applicant_address",
        "email",
        "phone",
        "application_number",
        "site_address",
        "development_description"
    ]
}

# Letter template settings
LETTER_CONFIG = {
    "template_file": "letter_template.docx",
    "output_format": "docx",  # Can be 'docx' or 'pdf'
    "font_name": "Arial",
    "font_size": 11
}

# CSV settings
CSV_CONFIG = {
    "filename_format": "planning_applications_{date}.csv",
    "date_format": "%Y-%m-%d"
}

# Logging settings
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "log_file": LOGS_DIR / "scraper.log"
}
