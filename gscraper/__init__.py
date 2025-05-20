import argparse
import json
import os
from .scraper import GScraper


def load_config():
    config_paths = [
        os.path.expanduser("~/.gscraper"),
        ".gscraper"
    ]
    config = {}
    for path in config_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                print(f"Loaded config from {path}")
                break
            except Exception as e:
                print(f"Error loading config from {path}: {e}")
    return config


def main():
    config = load_config()

    parser = argparse.ArgumentParser(
        description="G-scraper: A web scraper for.extracting text and documents from websites."
    )
    parser.add_argument("url", help="Starting URL to scrape")
    parser.add_argument(
        "--output-dir",
        default=config.get("output_dir", "gscraper_data"),
        help="Output directory for scraped data and documents"
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=config.get("max_pages", 1000),
        help="Maximum number of pages to scrape"
    )
    parser.add_argument(
        "--wait-time",
        type=float,
        default=config.get("wait_time", 5),
        help="Wait time for page loading (seconds)"
    )
    parser.add_argument(
        "--doc-extensions",
        default=config.get("doc_extensions", "pdf,doc,docx,xls,xlsx,csv"),
        help="Comma-separated list of document extensions to download"
    )
    parser.add_argument(
        "--max-concurrent",
        type=int,
        default=config.get("max_concurrent", 5),
        help="Maximum number of concurrent page requests"
    )

    args = parser.parse_args()

    doc_extensions = ['.' + ext.strip() for ext in args.doc_extensions.split(',')]
    scraper = GScraper(
        start_url=args.url,
        output_dir=args.output_dir,
        max_pages=args.max_pages,
        wait_time=args.wait_time,
        doc_extensions=doc_extensions,
        max_concurrent=args.max_concurrent
    )
    asyncio.run(scraper.scrape())


if __name__ == "__main__":
    main()