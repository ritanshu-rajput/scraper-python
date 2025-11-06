"""
Letter generator module for creating personalized letters
Supports both DOCX and PDF output formats
"""
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import re

logger = logging.getLogger(__name__)


class LetterGenerator:
    """Generates personalized letters from templates"""

    def __init__(self, config: dict, template_dir: Path):
        """
        Initialize the letter generator

        Args:
            config: Letter generation configuration
            template_dir: Directory containing letter templates
        """
        self.config = config
        self.template_dir = template_dir
        self.template_path = template_dir / config.get('template_file', 'letter_template.docx')

    def generate_letter(self, applicant_data: Dict, output_dir: Path) -> str:
        """
        Generate a personalized letter for an applicant

        Args:
            applicant_data: Dictionary with applicant details
            output_dir: Directory to save the generated letter

        Returns:
            Path to the generated letter file
        """
        try:
            # Create filename
            applicant_name = applicant_data.get('applicant_name', 'Unknown').replace(' ', '_')
            app_number = applicant_data.get('application_number', 'Unknown').replace('/', '_')
            filename = f"Letter_{app_number}_{applicant_name}.docx"
            output_path = output_dir / filename

            # Check if template exists
            if self.template_path.exists():
                logger.info(f"Using template: {self.template_path}")
                doc = self._load_and_fill_template(applicant_data)
            else:
                logger.warning(f"Template not found at {self.template_path}, creating default letter")
                doc = self._create_default_letter(applicant_data)

            # Save the document
            doc.save(str(output_path))
            logger.info(f"Letter generated: {output_path}")

            # Convert to PDF if requested
            if self.config.get('output_format') == 'pdf':
                pdf_path = self._convert_to_pdf(output_path)
                return str(pdf_path)

            return str(output_path)

        except Exception as e:
            logger.error(f"Error generating letter: {e}")
            raise

    def _load_and_fill_template(self, applicant_data: Dict) -> Document:
        """
        Load template and fill in placeholders

        Args:
            applicant_data: Dictionary with applicant details

        Returns:
            Filled document
        """
        doc = Document(str(self.template_path))

        # Define placeholders and their values
        placeholders = {
            '{APPLICANT_NAME}': applicant_data.get('applicant_name', 'N/A'),
            '{APPLICANT_ADDRESS}': applicant_data.get('applicant_address', 'N/A'),
            '{POSTCODE}': applicant_data.get('postcode', 'N/A'),
            '{EMAIL}': applicant_data.get('email', 'N/A'),
            '{PHONE}': applicant_data.get('phone', 'N/A'),
            '{APPLICATION_NUMBER}': applicant_data.get('application_number', 'N/A'),
            '{SITE_ADDRESS}': applicant_data.get('site_address', 'N/A'),
            '{DEVELOPMENT_DESCRIPTION}': applicant_data.get('development_description', 'N/A'),
            '{DATE}': datetime.now().strftime('%d %B %Y'),
        }

        # Replace placeholders in paragraphs
        for paragraph in doc.paragraphs:
            for placeholder, value in placeholders.items():
                if placeholder in paragraph.text:
                    paragraph.text = paragraph.text.replace(placeholder, str(value))

        # Replace placeholders in tables
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for placeholder, value in placeholders.items():
                        if placeholder in cell.text:
                            cell.text = cell.text.replace(placeholder, str(value))

        return doc

    def _create_default_letter(self, applicant_data: Dict) -> Document:
        """
        Create a default letter template

        Args:
            applicant_data: Dictionary with applicant details

        Returns:
            Document with default letter
        """
        doc = Document()

        # Set default margins
        sections = doc.sections
        for section in sections:
            section.top_margin = Inches(1)
            section.bottom_margin = Inches(1)
            section.left_margin = Inches(1)
            section.right_margin = Inches(1)

        # Add date
        date_paragraph = doc.add_paragraph()
        date_paragraph.add_run(datetime.now().strftime('%d %B %Y'))
        date_paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT

        # Add spacing
        doc.add_paragraph()

        # Add recipient address
        recipient_name = applicant_data.get('applicant_name', 'Dear Sir/Madam')
        recipient_address = applicant_data.get('applicant_address', '')

        if recipient_name != 'N/A':
            doc.add_paragraph(recipient_name)
        if recipient_address != 'N/A':
            # Split address into lines
            address_lines = recipient_address.split(',')
            for line in address_lines:
                doc.add_paragraph(line.strip())

        postcode = applicant_data.get('postcode', '')
        if postcode != 'N/A':
            doc.add_paragraph(postcode)

        # Add spacing
        doc.add_paragraph()

        # Add salutation
        salutation = f"Dear {recipient_name.split()[0] if recipient_name != 'N/A' else 'Sir/Madam'},"
        doc.add_paragraph(salutation)

        # Add subject line
        app_number = applicant_data.get('application_number', 'N/A')
        site_address = applicant_data.get('site_address', 'N/A')
        subject = doc.add_paragraph()
        subject_run = subject.add_run(f"Re: Planning Application {app_number} - {site_address}")
        subject_run.bold = True

        # Add spacing
        doc.add_paragraph()

        # Add body paragraphs
        body_text = f"""We are writing to you regarding your recent planning application ({app_number}) for the proposed development at {site_address}.

We would like to discuss your application further and explore potential opportunities that may be of interest to you.

{applicant_data.get('development_description', 'Your proposed development')} represents an important project, and we believe we may be able to assist you with professional services related to your application.

We would welcome the opportunity to arrange a convenient time to discuss your requirements in more detail.

Please feel free to contact us at your earliest convenience."""

        for para in body_text.split('\n\n'):
            if para.strip():
                doc.add_paragraph(para.strip())

        # Add closing
        doc.add_paragraph()
        doc.add_paragraph("Yours sincerely,")
        doc.add_paragraph()
        doc.add_paragraph()
        doc.add_paragraph("________________________")
        doc.add_paragraph("Your Name")
        doc.add_paragraph("Your Company Name")
        doc.add_paragraph("Contact Information")

        return doc

    def _convert_to_pdf(self, docx_path: Path) -> Path:
        """
        Convert DOCX to PDF (requires external tool or library)

        Args:
            docx_path: Path to DOCX file

        Returns:
            Path to PDF file
        """
        # Note: This requires either LibreOffice or docx2pdf
        # For simplicity, we'll use docx2pdf if available
        try:
            from docx2pdf import convert
            pdf_path = docx_path.with_suffix('.pdf')
            convert(str(docx_path), str(pdf_path))
            logger.info(f"Converted to PDF: {pdf_path}")
            return pdf_path
        except ImportError:
            logger.warning("docx2pdf not available, PDF conversion skipped")
            logger.info("Install docx2pdf or LibreOffice for PDF conversion")
            return docx_path
        except Exception as e:
            logger.error(f"PDF conversion failed: {e}")
            return docx_path

    def generate_batch(self, applicants_data: List[Dict], output_dir: Path) -> List[str]:
        """
        Generate letters for multiple applicants

        Args:
            applicants_data: List of applicant data dictionaries
            output_dir: Directory to save generated letters

        Returns:
            List of paths to generated letter files
        """
        generated_letters = []

        for i, applicant_data in enumerate(applicants_data, 1):
            try:
                logger.info(f"Generating letter {i}/{len(applicants_data)} for {applicant_data.get('applicant_name', 'Unknown')}")
                letter_path = self.generate_letter(applicant_data, output_dir)
                generated_letters.append(letter_path)
            except Exception as e:
                logger.error(f"Failed to generate letter for {applicant_data.get('applicant_name', 'Unknown')}: {e}")
                continue

        logger.info(f"Generated {len(generated_letters)} letters")
        return generated_letters

    def create_template(self, output_path: Path = None):
        """
        Create a sample letter template file

        Args:
            output_path: Path to save the template (optional)
        """
        if output_path is None:
            output_path = self.template_path

        doc = Document()

        # Set margins
        sections = doc.sections
        for section in sections:
            section.top_margin = Inches(1)
            section.bottom_margin = Inches(1)
            section.left_margin = Inches(1)
            section.right_margin = Inches(1)

        # Add instructions
        instructions = doc.add_paragraph()
        instructions_run = instructions.add_run("LETTER TEMPLATE - INSTRUCTIONS")
        instructions_run.bold = True
        doc.add_paragraph("Replace the placeholders below with your letter content.")
        doc.add_paragraph("Available placeholders:")
        placeholders_list = [
            "{DATE} - Current date",
            "{APPLICANT_NAME} - Applicant's full name",
            "{APPLICANT_ADDRESS} - Applicant's address",
            "{POSTCODE} - Applicant's postcode",
            "{EMAIL} - Applicant's email",
            "{PHONE} - Applicant's phone number",
            "{APPLICATION_NUMBER} - Planning application reference",
            "{SITE_ADDRESS} - Development site address",
            "{DEVELOPMENT_DESCRIPTION} - Description of proposed development"
        ]
        for item in placeholders_list:
            doc.add_paragraph(item, style='List Bullet')

        doc.add_paragraph()
        doc.add_paragraph("="*50)
        doc.add_paragraph()

        # Add template structure
        date_para = doc.add_paragraph()
        date_para.add_run("{DATE}")
        date_para.alignment = WD_ALIGN_PARAGRAPH.RIGHT

        doc.add_paragraph()
        doc.add_paragraph("{APPLICANT_NAME}")
        doc.add_paragraph("{APPLICANT_ADDRESS}")
        doc.add_paragraph("{POSTCODE}")

        doc.add_paragraph()
        doc.add_paragraph("Dear {APPLICANT_NAME},")

        subject = doc.add_paragraph()
        subject_run = subject.add_run("Re: Planning Application {APPLICATION_NUMBER} - {SITE_ADDRESS}")
        subject_run.bold = True

        doc.add_paragraph()
        doc.add_paragraph("[Your letter content goes here]")
        doc.add_paragraph()
        doc.add_paragraph("[You can reference the development: {DEVELOPMENT_DESCRIPTION}]")
        doc.add_paragraph()
        doc.add_paragraph("[Add more paragraphs as needed]")

        doc.add_paragraph()
        doc.add_paragraph("Yours sincerely,")
        doc.add_paragraph()
        doc.add_paragraph()
        doc.add_paragraph("[Your Name]")
        doc.add_paragraph("[Your Company]")
        doc.add_paragraph("[Your Contact Information]")

        # Save template
        doc.save(str(output_path))
        logger.info(f"Template created: {output_path}")
        print(f"\n✓ Template created at: {output_path}")
        print("  Edit this file to customize your letter template.")
