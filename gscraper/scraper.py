import time
import aiohttp
import asyncio
import os
import json
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from collections import deque
from datetime import datetime
from .utils import extract_text, download_document, is_valid_url

class GScraper:
    def __init__(self, start_url, output_dir="gscraper_data", max_pages=1000, wait_time=5, doc_extensions=None, max_concurrent=5):
        self.start_url = start_url
        self.output_dir = output_dir
        self.max_pages = max_pages
        self.wait_time = wait_time
        self.doc_extensions = doc_extensions or ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.csv']
        self.max_concurrent = max_concurrent  # Limit concurrent requests
        self.base_domain = urlparse(start_url).netloc
        self.driver = None
        self.visited = set()
        self.to_visit = deque()
        self.scraped_data = []
        self.semaphore = asyncio.Semaphore(max_concurrent)

    def setup_selenium(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)

    async def get_page_content(self, url, session):
        async with self.semaphore:
            try:
                # Use Selenium for dynamic content
                self.driver.get(url)
                time.sleep(self.wait_time)
                return self.driver.page_source
            except Exception as e:
                print(f"Error fetching {url}: {e}")
                return None

    async def extract_documents(self, soup, base_url, session):
        documents = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            if any(ext in full_url.lower() for ext in self.doc_extensions):
                doc_info = {
                    'title': link.get_text(strip=True) or full_url.split('/')[-1],
                    'url': full_url,
                    'file_path': None
                }
                download_dir = os.path.join(self.output_dir, "documents")
                file_path = await download_document(full_url, download_dir, session)
                if file_path:
                    doc_info['file_path'] = file_path
                    documents.append(doc_info)
        return documents

    def load_existing_data(self):
        output_file = os.path.join(self.output_dir, 'scraped_data.json')
        state_file = os.path.join(self.output_dir, 'crawler_state.json')
        self.scraped_data = []
        self.visited = set()
        self.to_visit = deque()

        if os.path.exists(output_file):
            try:
                with open(output_file, 'r', encoding='utf-8') as f:
                    self.scraped_data = json.load(f)
                self.visited = set(page['url'] for page in self.scraped_data)
                print(f"Loaded {len(self.scraped_data)} pages from existing data")
            except Exception as e:
                print(f"Error loading existing data: {e}")

        if os.path.exists(state_file):
            try:
                with open(state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                self.to_visit = deque(state.get('to_visit', []))
                print(f"Loaded {len(self.to_visit)} URLs to visit from state")
            except Exception as e:
                print(f"Error loading crawler state: {e}")

    def save_crawler_state(self):
        state_file = os.path.join(self.output_dir, 'crawler_state.json')
        state = {'to_visit': list(self.to_visit)}
        try:
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
            print(f"Crawler state saved: {len(self.to_visit)} URLs to visit")
        except Exception as e:
            print(f"Error saving crawler state: {e}")

    async def scrape_page(self, url, session):
        if url in self.visited:
            return

        print(f"Scraping: {url}")
        page_content = await self.get_page_content(url, session)
        if not page_content:
            return

        soup = BeautifulSoup(page_content, 'html.parser')
        self.visited.add(url)

        text = extract_text(soup)
        documents = await self.extract_documents(soup, url, session)

        page_data = {
            'url': url,
            'text': text,
            'documents': documents,
            'scraped_at': datetime.utcnow().isoformat()
        }
        self.scraped_data.append(page_data)

        for link in soup.find_all('a', href=True):
            next_url = urljoin(url, link['href'])
            if is_valid_url(next_url, self.base_domain) and next_url not in self.visited and next_url not in self.to_visit:
                self.to_visit.append(next_url)

    async def scrape(self):
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "documents"), exist_ok=True)

        self.load_existing_data()
        if not self.to_visit and self.start_url not in self.visited:
            self.to_visit.append(self.start_url)

        self.setup_selenium()
        page_count = len(self.scraped_data)

        try:
            async with aiohttp.ClientSession() as session:
                while self.to_visit and page_count < self.max_pages:
                    # Process up to max_concurrent pages at a time
                    batch_size = min(self.max_concurrent, len(self.to_visit), self.max_pages - page_count)
                    tasks = []
                    for _ in range(batch_size):
                        if self.to_visit:
                            url = self.to_visit.popleft()
                            tasks.append(self.scrape_page(url, session))
                    if tasks:
                        await asyncio.gather(*tasks, return_exceptions=True)
                        page_count = len(self.scraped_data)

                    # Save progress every 10 pages
                    if page_count % 10 == 0 or page_count >= self.max_pages:
                        output_file = os.path.join(self.output_dir, 'scraped_data.json')
                        with open(output_file, 'w', encoding='utf-8') as f:
                            json.dump(self.scraped_data, f, indent=2, ensure_ascii=False)
                        self.save_crawler_state()
                        print(f"Progress saved: {page_count} pages scraped")

        finally:
            if self.driver:
                self.driver.quit()

        output_file = os.path.join(self.output_dir, 'scraped_data.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.scraped_data, f, indent=2, ensure_ascii=False)
        self.save_crawler_state()

        print(f"Scraping complete. Data saved to {output_file}")
        print(f"Total pages scraped: {page_count}")
        print(f"Total documents downloaded: {sum(len(page['documents']) for page in self.scraped_data)}")