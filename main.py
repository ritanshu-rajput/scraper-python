#!/usr/bin/env python3
"""
Planning Application Scraper - Main CLI Script
Automates the process of scraping planning applications, extracting details, and generating letters
"""
import sys
import argparse
import logging
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from config import config
from src.modules.scraper import PlanningApplicationScraper
from src.modules.pdf_extractor import PDFExtractor
from src.modules.csv_handler import CSVHandler
from src.modules.letter_generator import LetterGenerator


def setup_logging(verbose: bool = False):
    """
    Set up logging configuration

    Args:
        verbose: Enable verbose (DEBUG) logging
    """
    log_level = logging.DEBUG if verbose else logging.INFO

    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format=config.LOGGING_CONFIG['format'],
        handlers=[
            logging.FileHandler(config.LOGGING_CONFIG['log_file']),
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Reduce noise from selenium and urllib3
    logging.getLogger('selenium').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)


def print_banner():
    """Print application banner"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║     Planning Application Scraper & Letter Generator       ║
╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def run_full_workflow(council: str, skip_scraping: bool = False, skip_letters: bool = False):
    """
    Run the complete workflow: scrape, extract, save CSV, generate letters

    Args:
        council: Council identifier
        skip_scraping: Skip scraping and use existing PDFs
        skip_letters: Skip letter generation
    """
    logger = logging.getLogger(__name__)

    try:
        # Get council configuration
        if council not in config.COUNCILS:
            logger.error(f"Unknown council: {council}")
            print(f"\n✗ Error: Council '{council}' not found in configuration")
            print(f"  Available councils: {', '.join(config.COUNCILS.keys())}")
            return False

        council_config = config.COUNCILS[council]
        if not council_config.get('enabled', False):
            logger.warning(f"Council {council} is disabled in configuration")
            print(f"\n⚠ Warning: Council '{council}' is disabled")
            return False

        print(f"\n▶ Processing: {council_config['name']}")
        print(f"  URL: {council_config['url']}")

        applications_data = []

        # Step 1: Scrape applications and download PDFs
        if not skip_scraping:
            print(f"\n[1/4] Scraping planning applications...")
            scraper = PlanningApplicationScraper(config.SCRAPER_CONFIG)

            applications = scraper.scrape_all_with_pdfs(
                council_config['url'],
                config.PDF_DIR
            )

            if not applications:
                print("  ✗ No applications found")
                return False

            print(f"  ✓ Found {len(applications)} applications")

            # Filter applications with PDFs
            apps_with_pdfs = [app for app in applications if app.get('pdf_path')]
            print(f"  ✓ Downloaded {len(apps_with_pdfs)} PDFs")

            if not apps_with_pdfs:
                print("  ✗ No PDFs downloaded successfully")
                return False

            applications_data = apps_with_pdfs

        else:
            print(f"\n[1/4] Skipping scraping (using existing PDFs)...")
            # Load existing PDFs
            pdf_files = list(config.PDF_DIR.glob("*.pdf"))
            if not pdf_files:
                print(f"  ✗ No PDFs found in {config.PDF_DIR}")
                return False

            print(f"  ✓ Found {len(pdf_files)} existing PDFs")
            applications_data = [{'pdf_path': str(pdf)} for pdf in pdf_files]

        # Step 2: Extract details from PDFs
        print(f"\n[2/4] Extracting applicant details from PDFs...")
        extractor = PDFExtractor(config.PDF_CONFIG)

        for app in applications_data:
            if app.get('pdf_path'):
                try:
                    details = extractor.extract_applicant_details(app['pdf_path'])
                    # Merge extracted details with application data
                    app.update(details)
                except Exception as e:
                    logger.error(f"Failed to extract from {app['pdf_path']}: {e}")

        # Filter out applications without names
        valid_applications = [app for app in applications_data if app.get('applicant_name') != 'N/A']
        print(f"  ✓ Extracted details from {len(valid_applications)} applications")

        if not valid_applications:
            print("  ✗ No valid applicant details extracted")
            return False

        # Step 3: Save to CSV
        print(f"\n[3/4] Saving data to CSV...")
        csv_handler = CSVHandler(config.CSV_CONFIG)

        csv_path = csv_handler.save_to_csv(valid_applications, config.CSV_DIR)
        print(f"  ✓ Saved to: {csv_path}")

        # Also create a contact list
        contact_list_path = config.CSV_DIR / f"contact_list_{datetime.now().strftime('%Y-%m-%d')}.csv"
        csv_handler.export_contact_list(csv_path, str(contact_list_path))
        print(f"  ✓ Contact list: {contact_list_path}")

        # Step 4: Generate letters
        if not skip_letters:
            print(f"\n[4/4] Generating personalized letters...")
            letter_generator = LetterGenerator(config.LETTER_CONFIG, config.TEMPLATES_DIR)

            letters = letter_generator.generate_batch(valid_applications, config.LETTERS_DIR)
            print(f"  ✓ Generated {len(letters)} letters in: {config.LETTERS_DIR}")
        else:
            print(f"\n[4/4] Skipping letter generation")

        # Summary
        print("\n" + "="*60)
        print("✓ WORKFLOW COMPLETED SUCCESSFULLY")
        print("="*60)
        print(f"  Applications processed: {len(valid_applications)}")
        print(f"  CSV file: {csv_path}")
        print(f"  Contact list: {contact_list_path}")
        if not skip_letters:
            print(f"  Letters directory: {config.LETTERS_DIR}")
        print("="*60)

        return True

    except KeyboardInterrupt:
        print("\n\n✗ Process interrupted by user")
        return False
    except Exception as e:
        logger.error(f"Workflow failed: {e}", exc_info=True)
        print(f"\n✗ Error: {e}")
        print(f"  Check logs at: {config.LOGGING_CONFIG['log_file']}")
        return False


def create_template_command():
    """Create a sample letter template"""
    logger = logging.getLogger(__name__)

    try:
        print("\n▶ Creating letter template...")
        letter_generator = LetterGenerator(config.LETTER_CONFIG, config.TEMPLATES_DIR)
        letter_generator.create_template()
        print("✓ Template creation completed")
        return True
    except Exception as e:
        logger.error(f"Failed to create template: {e}")
        print(f"✗ Error: {e}")
        return False


def list_councils_command():
    """List available councils"""
    print("\n▶ Available Councils:")
    print("="*60)

    for council_id, council_info in config.COUNCILS.items():
        status = "✓ Enabled" if council_info.get('enabled', False) else "✗ Disabled"
        print(f"\n  {council_info['name']}")
        print(f"    ID: {council_id}")
        print(f"    Status: {status}")
        print(f"    URL: {council_info['url']}")

    print("\n" + "="*60)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Planning Application Scraper & Letter Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run full workflow for South Lanarkshire
  python main.py run south_lanarkshire

  # Run without generating letters
  python main.py run south_lanarkshire --skip-letters

  # Use existing PDFs (skip scraping)
  python main.py run south_lanarkshire --skip-scraping

  # Create letter template
  python main.py create-template

  # List available councils
  python main.py list-councils
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Run command
    run_parser = subparsers.add_parser('run', help='Run the scraper workflow')
    run_parser.add_argument('council', help='Council identifier (e.g., south_lanarkshire)')
    run_parser.add_argument('--skip-scraping', action='store_true',
                           help='Skip scraping and use existing PDFs')
    run_parser.add_argument('--skip-letters', action='store_true',
                           help='Skip letter generation')
    run_parser.add_argument('-v', '--verbose', action='store_true',
                           help='Enable verbose logging')

    # Create template command
    template_parser = subparsers.add_parser('create-template',
                                           help='Create a sample letter template')

    # List councils command
    list_parser = subparsers.add_parser('list-councils',
                                       help='List available councils')

    # Parse arguments
    args = parser.parse_args()

    # Show help if no command provided
    if not args.command:
        parser.print_help()
        return 0

    # Print banner
    print_banner()

    # Set up logging
    verbose = getattr(args, 'verbose', False)
    setup_logging(verbose)

    # Execute command
    if args.command == 'run':
        success = run_full_workflow(
            args.council,
            skip_scraping=args.skip_scraping,
            skip_letters=args.skip_letters
        )
        return 0 if success else 1

    elif args.command == 'create-template':
        success = create_template_command()
        return 0 if success else 1

    elif args.command == 'list-councils':
        list_councils_command()
        return 0

    return 0


if __name__ == '__main__':
    sys.exit(main())
