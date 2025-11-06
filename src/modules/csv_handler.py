"""
CSV handler module for storing extracted application data
"""
import csv
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger(__name__)


class CSVHandler:
    """Handles CSV operations for storing application data"""

    def __init__(self, config: dict):
        """
        Initialize the CSV handler

        Args:
            config: CSV configuration dictionary
        """
        self.config = config

    def save_to_csv(self, data: List[Dict], output_dir: Path, filename: str = None) -> str:
        """
        Save application data to CSV file

        Args:
            data: List of dictionaries with application data
            output_dir: Directory to save the CSV file
            filename: Custom filename (optional)

        Returns:
            Path to the saved CSV file
        """
        if not data:
            logger.warning("No data to save to CSV")
            return None

        # Generate filename if not provided
        if not filename:
            date_str = datetime.now().strftime(self.config.get('date_format', '%Y-%m-%d'))
            filename = self.config.get('filename_format', 'planning_applications_{date}.csv').format(date=date_str)

        csv_path = output_dir / filename

        try:
            # Define CSV columns
            fieldnames = [
                'application_number',
                'applicant_name',
                'applicant_address',
                'postcode',
                'email',
                'phone',
                'site_address',
                'development_description',
                'status',
                'pdf_filename',
                'pdf_path',
                'application_url',
                'extraction_date'
            ]

            # Add extraction date to each record
            extraction_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            for record in data:
                record['extraction_date'] = extraction_date

            # Write to CSV
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
                writer.writeheader()

                for record in data:
                    # Ensure all fields exist
                    row = {field: record.get(field, 'N/A') for field in fieldnames}
                    writer.writerow(row)

            logger.info(f"Saved {len(data)} records to CSV: {csv_path}")
            return str(csv_path)

        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")
            raise

    def read_from_csv(self, csv_path: str) -> List[Dict]:
        """
        Read application data from CSV file

        Args:
            csv_path: Path to CSV file

        Returns:
            List of dictionaries with application data
        """
        try:
            data = []
            with open(csv_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    data.append(dict(row))

            logger.info(f"Read {len(data)} records from CSV: {csv_path}")
            return data

        except Exception as e:
            logger.error(f"Error reading from CSV: {e}")
            raise

    def append_to_csv(self, data: List[Dict], csv_path: str):
        """
        Append data to existing CSV file

        Args:
            data: List of dictionaries with application data
            csv_path: Path to CSV file
        """
        try:
            # Read existing data
            existing_data = []
            if Path(csv_path).exists():
                existing_data = self.read_from_csv(csv_path)

            # Combine and remove duplicates based on application_number
            all_data = existing_data + data
            unique_data = {record['application_number']: record for record in all_data}
            unique_data_list = list(unique_data.values())

            # Save back to CSV
            self.save_to_csv(unique_data_list, Path(csv_path).parent, Path(csv_path).name)

            logger.info(f"Appended {len(data)} records to CSV: {csv_path}")

        except Exception as e:
            logger.error(f"Error appending to CSV: {e}")
            raise

    def export_contact_list(self, csv_path: str, output_path: str):
        """
        Export a simplified contact list with just names and addresses

        Args:
            csv_path: Path to source CSV file
            output_path: Path for output contact list CSV
        """
        try:
            data = self.read_from_csv(csv_path)

            # Create simplified contact list
            contacts = []
            for record in data:
                contact = {
                    'name': record.get('applicant_name', 'N/A'),
                    'address': record.get('applicant_address', 'N/A'),
                    'postcode': record.get('postcode', 'N/A'),
                    'email': record.get('email', 'N/A'),
                    'phone': record.get('phone', 'N/A')
                }
                contacts.append(contact)

            # Write to CSV
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['name', 'address', 'postcode', 'email', 'phone']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(contacts)

            logger.info(f"Exported {len(contacts)} contacts to: {output_path}")

        except Exception as e:
            logger.error(f"Error exporting contact list: {e}")
            raise
