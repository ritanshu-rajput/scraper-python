"""
PDF extraction module for planning application forms
Extracts applicant details and contact information from PDFs
"""
import logging
import re
from pathlib import Path
from typing import Dict, Optional
import PyPDF2

# Make pdfplumber optional
try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False
    logging.warning("pdfplumber not available, will use PyPDF2 only")

logger = logging.getLogger(__name__)


class PDFExtractor:
    """Extracts applicant information from planning application PDFs"""

    def __init__(self, config: dict):
        """
        Initialize the PDF extractor

        Args:
            config: PDF extraction configuration
        """
        self.config = config

    def extract_applicant_details(self, pdf_path: str) -> Dict:
        """
        Extract applicant details from a PDF

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Dictionary with extracted details
        """
        logger.info(f"Extracting details from: {pdf_path}")

        # Try both extraction methods
        text = self._extract_text_pdfplumber(pdf_path)
        if not text or len(text.strip()) < 100:
            logger.info("Trying alternative extraction method (PyPDF2)")
            text = self._extract_text_pypdf2(pdf_path)

        if not text:
            logger.error(f"Failed to extract text from {pdf_path}")
            return self._create_empty_details()

        # Extract details using regex patterns
        details = self._parse_applicant_info(text)

        # Add PDF path
        details['pdf_path'] = pdf_path
        details['pdf_filename'] = Path(pdf_path).name

        logger.info(f"Extracted details for: {details.get('applicant_name', 'Unknown')}")
        return details

    def _extract_text_pdfplumber(self, pdf_path: str) -> Optional[str]:
        """
        Extract text using pdfplumber (better for forms)

        Args:
            pdf_path: Path to PDF file

        Returns:
            Extracted text or None
        """
        if not PDFPLUMBER_AVAILABLE:
            return None

        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
                return text
        except Exception as e:
            logger.error(f"pdfplumber extraction failed: {e}")
            return None

    def _extract_text_pypdf2(self, pdf_path: str) -> Optional[str]:
        """
        Extract text using PyPDF2 (fallback method)

        Args:
            pdf_path: Path to PDF file

        Returns:
            Extracted text or None
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() or ""
                return text
        except Exception as e:
            logger.error(f"PyPDF2 extraction failed: {e}")
            return None

    def _parse_applicant_info(self, text: str) -> Dict:
        """
        Parse applicant information from extracted text using patterns

        Args:
            text: Extracted PDF text

        Returns:
            Dictionary with parsed information
        """
        details = self._create_empty_details()

        # Clean the text
        text = text.replace('\n', ' ').replace('\r', ' ')
        text = re.sub(r'\s+', ' ', text)

        # Extract application number/reference
        ref_patterns = [
            r'Application\s+(?:Reference|Number|No\.?)\s*:?\s*([A-Z0-9/\-]+)',
            r'Reference\s*:?\s*([A-Z0-9/\-]+)',
            r'App(?:lication)?\s+Ref\s*:?\s*([A-Z0-9/\-]+)'
        ]
        details['application_number'] = self._extract_with_patterns(text, ref_patterns)

        # Extract applicant name
        name_patterns = [
            r'Applicant\s+Name\s*:?\s*([A-Z][a-zA-Z\s\-\.]+?)(?:\s+Address|Agent|Telephone|\d{2,})',
            r'Name\s+of\s+Applicant\s*:?\s*([A-Z][a-zA-Z\s\-\.]+?)(?:\s+Address|Agent|Telephone|\d{2,})',
            r'Applicant\s*:?\s*([A-Z][a-zA-Z\s\-\.]+?)(?:\s+Address|Agent|Telephone|\d{2,})',
            r'(?:Mr|Mrs|Ms|Miss|Dr)\s+([A-Z][a-zA-Z\s\-\.]+?)(?:\s+\d|\s+[A-Z]{2}\d)',
        ]
        applicant_name = self._extract_with_patterns(text, name_patterns)
        if applicant_name:
            applicant_name = self._clean_name(applicant_name)
        details['applicant_name'] = applicant_name

        # Extract applicant address
        address_patterns = [
            r'Applicant[^:]*Address\s*:?\s*([A-Z0-9][^:]+?)(?=\s*Post\s*code|Email|Telephone|Agent)',
            r'Address\s+of\s+Applicant\s*:?\s*([A-Z0-9][^:]+?)(?=\s*Post\s*code|Email|Telephone|Agent)',
            r'Applicant.*?Address\s*:?\s*([A-Z0-9][^:]+?)(?=\s*Post\s*code|Email|Telephone|Agent)',
        ]
        applicant_address = self._extract_with_patterns(text, address_patterns)
        if applicant_address:
            applicant_address = self._clean_address(applicant_address)
        details['applicant_address'] = applicant_address

        # Extract postcode
        postcode_pattern = r'\b([A-Z]{1,2}\d{1,2}[A-Z]?\s?\d[A-Z]{2})\b'
        postcode_match = re.search(postcode_pattern, text)
        if postcode_match and applicant_address:
            details['postcode'] = postcode_match.group(1)

        # Extract email
        email_patterns = [
            r'[Ee]mail\s*:?\s*([\w\.-]+@[\w\.-]+\.\w+)',
            r'[Ee]-mail\s*:?\s*([\w\.-]+@[\w\.-]+\.\w+)',
            r'\b([\w\.-]+@[\w\.-]+\.\w+)\b'
        ]
        details['email'] = self._extract_with_patterns(text, email_patterns)

        # Extract phone number
        phone_patterns = [
            r'[Tt]elephone\s*:?\s*([\d\s\-\(\)]{10,})',
            r'[Pp]hone\s*:?\s*([\d\s\-\(\)]{10,})',
            r'[Mm]obile\s*:?\s*([\d\s\-\(\)]{10,})',
            r'[Cc]ontact\s+[Nn]umber\s*:?\s*([\d\s\-\(\)]{10,})',
        ]
        phone = self._extract_with_patterns(text, phone_patterns)
        if phone:
            phone = self._clean_phone(phone)
        details['phone'] = phone

        # Extract site address (development location)
        site_patterns = [
            r'Site\s+Address\s*:?\s*([A-Z0-9][^:]+?)(?=\s*Description|Proposal|Postcode|Grid)',
            r'Location\s*:?\s*([A-Z0-9][^:]+?)(?=\s*Description|Proposal|Postcode|Grid)',
            r'Address\s+of\s+[Dd]evelopment\s*:?\s*([A-Z0-9][^:]+?)(?=\s*Description|Proposal|Postcode)',
        ]
        site_address = self._extract_with_patterns(text, site_patterns)
        if site_address:
            site_address = self._clean_address(site_address)
        details['site_address'] = site_address

        # Extract development description
        desc_patterns = [
            r'Description\s+of\s+[Pp]roposed\s+[Dd]evelopment\s*:?\s*(.{10,200}?)(?=\s*[A-Z][a-z]+\s*:|$)',
            r'[Pp]roposal\s*:?\s*(.{10,200}?)(?=\s*[A-Z][a-z]+\s*:|$)',
            r'[Dd]evelopment\s+[Dd]escription\s*:?\s*(.{10,200}?)(?=\s*[A-Z][a-z]+\s*:|$)',
        ]
        description = self._extract_with_patterns(text, desc_patterns)
        if description:
            description = description.strip()[:200]  # Limit length
        details['development_description'] = description

        return details

    def _extract_with_patterns(self, text: str, patterns: list) -> str:
        """
        Try multiple regex patterns to extract information

        Args:
            text: Text to search
            patterns: List of regex patterns

        Returns:
            Extracted text or "N/A"
        """
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                result = match.group(1).strip()
                if result and len(result) > 2:
                    return result
        return "N/A"

    def _clean_name(self, name: str) -> str:
        """Clean and format extracted name"""
        # Remove extra whitespace
        name = re.sub(r'\s+', ' ', name).strip()
        # Remove trailing punctuation
        name = name.rstrip('.,;:')
        # Capitalize properly
        name = ' '.join(word.capitalize() for word in name.split())
        return name

    def _clean_address(self, address: str) -> str:
        """Clean and format extracted address"""
        # Remove extra whitespace
        address = re.sub(r'\s+', ' ', address).strip()
        # Remove trailing punctuation
        address = address.rstrip('.,;:')
        return address

    def _clean_phone(self, phone: str) -> str:
        """Clean and format phone number"""
        # Keep only digits, spaces, and common separators
        phone = re.sub(r'[^\d\s\-\(\)]', '', phone).strip()
        return phone

    def _create_empty_details(self) -> Dict:
        """Create dictionary with empty/default values"""
        return {
            'applicant_name': 'N/A',
            'applicant_address': 'N/A',
            'postcode': 'N/A',
            'email': 'N/A',
            'phone': 'N/A',
            'application_number': 'N/A',
            'site_address': 'N/A',
            'development_description': 'N/A',
            'pdf_path': None,
            'pdf_filename': None
        }

    def extract_batch(self, pdf_paths: list) -> list:
        """
        Extract details from multiple PDFs

        Args:
            pdf_paths: List of PDF file paths

        Returns:
            List of dictionaries with extracted details
        """
        results = []
        for pdf_path in pdf_paths:
            try:
                details = self.extract_applicant_details(pdf_path)
                results.append(details)
            except Exception as e:
                logger.error(f"Error extracting from {pdf_path}: {e}")
                empty_details = self._create_empty_details()
                empty_details['pdf_path'] = pdf_path
                results.append(empty_details)

        logger.info(f"Extracted details from {len(results)} PDFs")
        return results
