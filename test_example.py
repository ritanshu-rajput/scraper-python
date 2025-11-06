#!/usr/bin/env python3
"""
Simple test script to verify core functionality
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.modules.csv_handler import CSVHandler
from src.modules.letter_generator import LetterGenerator
from config import config

def test_csv_and_letters():
    """Test CSV handling and letter generation"""

    print("Testing CSV and Letter Generation...")
    print("="*60)

    # Sample data
    sample_data = [
        {
            'application_number': 'P/2024/0001',
            'applicant_name': 'John Smith',
            'applicant_address': '123 Main Street, Glasgow',
            'postcode': 'G1 1AA',
            'email': 'john.smith@email.com',
            'phone': '0141 123 4567',
            'site_address': '456 Oak Avenue, Glasgow',
            'development_description': 'Construction of single storey rear extension',
            'status': 'Pending',
            'pdf_filename': 'P_2024_0001.pdf',
            'pdf_path': '/path/to/pdf',
            'application_url': 'https://example.com/app1'
        },
        {
            'application_number': 'P/2024/0002',
            'applicant_name': 'Jane Doe',
            'applicant_address': '789 High Street, Lanark',
            'postcode': 'ML11 9AB',
            'email': 'jane.doe@email.com',
            'phone': '01555 123 4567',
            'site_address': '321 Park Road, Lanark',
            'development_description': 'Erection of detached garage',
            'status': 'Pending',
            'pdf_filename': 'P_2024_0002.pdf',
            'pdf_path': '/path/to/pdf',
            'application_url': 'https://example.com/app2'
        }
    ]

    # Test CSV Handler
    print("\n1. Testing CSV Handler...")
    csv_handler = CSVHandler(config.CSV_CONFIG)

    csv_path = csv_handler.save_to_csv(sample_data, config.CSV_DIR, "test_applications.csv")
    print(f"   ✓ CSV saved: {csv_path}")

    # Read back
    read_data = csv_handler.read_from_csv(csv_path)
    print(f"   ✓ CSV read: {len(read_data)} records")

    # Test contact list export
    contact_list_path = config.CSV_DIR / "test_contacts.csv"
    csv_handler.export_contact_list(csv_path, str(contact_list_path))
    print(f"   ✓ Contact list exported: {contact_list_path}")

    # Test Letter Generator
    print("\n2. Testing Letter Generator...")
    letter_generator = LetterGenerator(config.LETTER_CONFIG, config.TEMPLATES_DIR)

    letters = letter_generator.generate_batch(sample_data, config.LETTERS_DIR)
    print(f"   ✓ Generated {len(letters)} letters")
    for letter in letters:
        print(f"      - {Path(letter).name}")

    print("\n" + "="*60)
    print("✓ All tests passed!")
    print("="*60)
    print(f"\nCheck outputs in:")
    print(f"  - CSV: {config.CSV_DIR}")
    print(f"  - Letters: {config.LETTERS_DIR}")

if __name__ == '__main__':
    test_csv_and_letters()
