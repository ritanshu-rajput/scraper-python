"""
Web scraper module for planning applications
Uses Selenium for robust web scraping with anti-bot protection handling
"""
import time
import logging
from pathlib import Path
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import requests

logger = logging.getLogger(__name__)


class PlanningApplicationScraper:
    """Scrapes planning applications from council websites"""

    def __init__(self, config: dict):
        """
        Initialize the scraper

        Args:
            config: Scraper configuration dictionary
        """
        self.config = config
        self.driver = None
        self.applications = []

    def _setup_driver(self):
        """Set up Selenium WebDriver with appropriate options"""
        chrome_options = Options()

        if self.config.get('headless', True):
            chrome_options.add_argument('--headless')

        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument(f'user-agent={self.config.get("user_agent")}')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # Disable images and CSS for faster loading (optional)
        prefs = {
            'profile.managed_default_content_settings.images': 2,
            'profile.managed_default_content_settings.stylesheets': 2
        }
        chrome_options.add_experimental_option('prefs', prefs)

        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            logger.info("WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise

    def _close_driver(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            logger.info("WebDriver closed")

    def scrape_weekly_applications(self, council_url: str) -> List[Dict]:
        """
        Scrape weekly planning applications from a council website

        Args:
            council_url: URL to the weekly applications list

        Returns:
            List of application dictionaries with details and PDF links
        """
        self.applications = []

        try:
            self._setup_driver()
            logger.info(f"Accessing weekly applications at: {council_url}")

            # Navigate to the weekly list page
            self.driver.get(council_url)
            time.sleep(3)  # Wait for page to load

            # Wait for the results table to load
            wait = WebDriverWait(self.driver, self.config.get('timeout', 30))

            try:
                # Try to find the results table
                wait.until(EC.presence_of_element_located((By.ID, "searchResultsTable")))
                logger.info("Applications table loaded")
            except TimeoutException:
                logger.warning("Results table not found with ID 'searchResultsTable', trying alternative selectors")
                # Try alternative selectors
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "searchresults")))

            # Get page source and parse with BeautifulSoup
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')

            # Find all application rows
            application_rows = soup.find_all('tr', class_='searchresult')

            if not application_rows:
                # Try alternative row selector
                application_rows = soup.select('#searchResultsTable tbody tr')

            logger.info(f"Found {len(application_rows)} applications")

            for row in application_rows:
                try:
                    app_data = self._extract_application_data(row)
                    if app_data:
                        self.applications.append(app_data)
                except Exception as e:
                    logger.error(f"Error extracting application data: {e}")
                    continue

            logger.info(f"Successfully extracted {len(self.applications)} applications")

        except Exception as e:
            logger.error(f"Error during scraping: {e}")
            raise
        finally:
            self._close_driver()

        return self.applications

    def _extract_application_data(self, row) -> Optional[Dict]:
        """
        Extract application data from a table row

        Args:
            row: BeautifulSoup row element

        Returns:
            Dictionary with application data or None
        """
        try:
            # Find the application link
            link_elem = row.find('a', href=True)
            if not link_elem:
                return None

            application_url = link_elem['href']
            if not application_url.startswith('http'):
                application_url = 'https://publicaccess.southlanarkshire.gov.uk' + application_url

            # Extract application reference
            application_ref = link_elem.text.strip()

            # Extract address (usually in the second column)
            columns = row.find_all('td')
            address = columns[1].text.strip() if len(columns) > 1 else "N/A"

            # Extract proposal description
            proposal = columns[2].text.strip() if len(columns) > 2 else "N/A"

            # Extract status
            status = columns[3].text.strip() if len(columns) > 3 else "N/A"

            app_data = {
                'reference': application_ref,
                'url': application_url,
                'address': address,
                'proposal': proposal,
                'status': status,
                'pdf_url': None,
                'pdf_path': None
            }

            logger.debug(f"Extracted application: {application_ref}")
            return app_data

        except Exception as e:
            logger.error(f"Error extracting row data: {e}")
            return None

    def get_application_pdf(self, application: Dict, download_dir: Path) -> Optional[str]:
        """
        Navigate to application details and download the PDF

        Args:
            application: Application dictionary
            download_dir: Directory to save PDFs

        Returns:
            Path to downloaded PDF or None
        """
        try:
            self._setup_driver()

            logger.info(f"Accessing application: {application['reference']}")
            self.driver.get(application['url'])
            time.sleep(2)

            # Click on Documents tab
            try:
                documents_tab = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Documents"))
                )
                documents_tab.click()
                time.sleep(2)
                logger.info("Documents tab opened")
            except Exception as e:
                logger.warning(f"Could not click Documents tab: {e}")
                # Try alternative selectors
                try:
                    documents_tab = self.driver.find_element(By.PARTIAL_LINK_TEXT, "Document")
                    documents_tab.click()
                    time.sleep(2)
                except:
                    logger.error("Failed to find Documents tab")
                    return None

            # Find Application Form PDF link
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')

            # Look for links containing "Application Form" or similar
            pdf_links = soup.find_all('a', href=True)
            application_form_link = None

            for link in pdf_links:
                link_text = link.text.lower()
                if 'application' in link_text and ('form' in link_text or 'pdf' in link.get('href', '').lower()):
                    application_form_link = link['href']
                    break

            if not application_form_link:
                logger.warning(f"No application form PDF found for {application['reference']}")
                return None

            # Ensure full URL
            if not application_form_link.startswith('http'):
                application_form_link = 'https://publicaccess.southlanarkshire.gov.uk' + application_form_link

            application['pdf_url'] = application_form_link

            # Download the PDF
            pdf_path = self._download_pdf(application_form_link, application['reference'], download_dir)
            application['pdf_path'] = pdf_path

            return pdf_path

        except Exception as e:
            logger.error(f"Error getting PDF for {application['reference']}: {e}")
            return None
        finally:
            self._close_driver()

    def _download_pdf(self, pdf_url: str, reference: str, download_dir: Path) -> Optional[str]:
        """
        Download a PDF file

        Args:
            pdf_url: URL of the PDF
            reference: Application reference for filename
            download_dir: Directory to save the PDF

        Returns:
            Path to downloaded PDF or None
        """
        try:
            # Clean the reference for use as filename
            safe_ref = reference.replace('/', '_').replace('\\', '_')
            pdf_filename = f"{safe_ref}.pdf"
            pdf_path = download_dir / pdf_filename

            logger.info(f"Downloading PDF from: {pdf_url}")

            headers = {
                'User-Agent': self.config.get('user_agent')
            }

            response = requests.get(pdf_url, headers=headers, timeout=30)
            response.raise_for_status()

            with open(pdf_path, 'wb') as f:
                f.write(response.content)

            logger.info(f"PDF saved to: {pdf_path}")
            return str(pdf_path)

        except Exception as e:
            logger.error(f"Error downloading PDF: {e}")
            return None

    def scrape_all_with_pdfs(self, council_url: str, download_dir: Path) -> List[Dict]:
        """
        Complete scraping workflow: get applications and download PDFs

        Args:
            council_url: URL to the weekly applications list
            download_dir: Directory to save PDFs

        Returns:
            List of applications with PDF paths
        """
        # First, get all applications
        applications = self.scrape_weekly_applications(council_url)

        logger.info(f"Processing {len(applications)} applications for PDF download")

        # Then download PDFs for each
        for i, app in enumerate(applications, 1):
            logger.info(f"Processing application {i}/{len(applications)}: {app['reference']}")
            try:
                self.get_application_pdf(app, download_dir)
                time.sleep(self.config.get('download_delay', 2))
            except Exception as e:
                logger.error(f"Failed to process {app['reference']}: {e}")
                continue

        # Filter out applications without PDFs
        successful_apps = [app for app in applications if app.get('pdf_path')]
        logger.info(f"Successfully downloaded {len(successful_apps)} PDFs")

        return applications
