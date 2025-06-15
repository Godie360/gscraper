<p align="center">
  <img src="./ChatGPT%20Image%20Jun%2014,%202025,%2002_02_52%20PM.png" alt="G-scraper Logo" width="200"/>
</p>


# G-scraper

G-scraper is a Python tool for scraping text and documents (e.g., PDFs, DOCX, XLSX) from websites. It supports resuming interrupted sessions, parallel scraping for efficiency, and customizable settings via a configuration file or command-line arguments.

## Features

- **Comprehensive Scraping**: Extracts text and downloads documents from websites.
- **Resume Capability**: Continues scraping from where it left off if interrupted.
- **Parallel Scraping**: Uses asynchronous requests to scrape multiple pages concurrently, improving speed.
- **Config File**: Supports a `.gscraper` file for default settings.
- **Customizable**: Configure output directory, maximum pages, wait time, document types, and concurrent requests.

## Installation

1. **Install Python**: Ensure Python 3.6 or higher is installed.
2. **Install Chrome and ChromeDriver**:
   - On Ubuntu/Debian:
     ```bash
     sudo apt-get install chromium-chromedriver
     ```
   - Or download from [ChromeDriver](https://chromedriver.chromium.org/downloads) and add to your PATH.
3. **Install G-scraper**:
   ```bash
   pip install gscraper
   ```
   Alternatively, install from GitHub:
   ```bash
   pip install git+https://github.com/yourusername/gscraper.git
   ```

## Configuration

Create a `.gscraper` file in your home directory (`~/.gscraper`) or project root to set default settings. Copy the `sample.gscraper` file from the package:

```json
{
  "output_dir": "gscraper_data",
  "max_pages": 1000,
  "wait_time": 5,
  "doc_extensions": "pdf,doc,docx,xls,xlsx,csv",
  "max_concurrent": 5
}
```

Edit the file to customize defaults. Command-line arguments override these settings.

## Usage

Run G-scraper from the command line:

```bash
gscraper <start_url> [--output-dir <dir>] [--max-pages <num>] [--wait-time <seconds>] [--doc-extensions <exts>] [--max-concurrent <num>]
```

### Options

- `<start_url>`: Starting URL to scrape (e.g., `https://www.nbs.go.tz/`).
- `--output-dir`: Output directory for data and documents (default: `gscraper_data`).
- `--max-pages`: Maximum number of pages to scrape (default: 1000).
- `--wait-time`: Wait time for page loading in seconds (default: 5).
- `--doc-extensions`: Comma-separated list of document extensions to download (default: `pdf,doc,docx,xls,xlsx,csv`).
- `--max-concurrent`: Maximum number of concurrent page requests (default: 5).

### Example

```bash
gscraper https://www.nbs.go.tz/ --output-dir nbs_data --max-pages 500 --wait-time 3 --max-concurrent 10
```

This command scrapes up to 500 pages from `https://www.nbs.go.tz/` with up to 10 concurrent requests, saving data to `nbs_data`, and waits 3 seconds per page for dynamic content to load.

## Resuming

If interrupted (e.g., by Ctrl+C), G-scraper resumes from the last saved state when rerun with the same `--output-dir`. It skips already scraped pages and documents, ensuring no duplicate work.

## Output

The output is saved in the specified `--output-dir` (default: `gscraper_data`):

- **`scraped_data.json`**: JSON file containing scraped page data, including URLs, text, documents, and timestamps.
- **`crawler_state.json`**: State file with URLs yet to be visited, used for resuming.
- **`documents/`**: Directory containing downloaded documents (e.g., PDFs, DOCX).

Example `scraped_data.json` snippet:

```json
[
  {
    "url": "https://www.nbs.go.tz/",
    "text": "Welcome to National Bureau of Statistics ...",
    "documents": [
      {
        "title": "Annual Report 2023",
        "url": "https://www.nbs.go.tz/reports/annual_report_2023.pdf",
        "file_path": "nbs_data/documents/annual_report_2023.pdf"
      }
    ],
    "scraped_at": "2025-05-20T09:53:00Z"
  }
]
```

## Notes

- **Parallel Scraping**: G-scraper uses asynchronous requests to fetch pages and documents concurrently, controlled by `--max-concurrent`. Adjust this value to balance speed and server load (e.g., 5–10 is typically safe).
- **Ethical Scraping**: Always check the target website’s `robots.txt` and terms of service. Use `--wait-time` and `--max-concurrent` to avoid overwhelming servers. G-scraper includes delays and limits to promote responsible scraping.
- **Selenium Dependency**: G-scraper uses Selenium for dynamic content, requiring Chrome and ChromeDriver. For static sites, future versions may support purely asynchronous scraping.
- **Config File**: If no `.gscraper` file is found, defaults are used. Command-line arguments always take precedence.

## Troubleshooting

- **ChromeDriver Errors**: Ensure ChromeDriver is in your PATH and matches your Chrome version.
- **Connection Issues**: Increase `--wait-time` or reduce `--max-concurrent` if requests fail frequently.
- **Disk Space**: Large websites may generate many documents; ensure sufficient disk space.

## License

MIT License. See [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Fork the repository, make changes, and submit a pull request. For issues or feature requests, open an issue on [GitHub](https://github.com/Godie360/gscraper).

## Contact

For questions, contact [Godfrey Enosh](https://godfreyenosh.netlify.app/) at [godfreyenos360@gmail.com](godfreyenos360@gmail.com).
