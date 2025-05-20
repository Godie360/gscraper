import re
import os
import aiohttp
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def extract_text(soup):
    for tag in soup(["script", "style"]):
        tag.decompose()
    text = soup.get_text(separator=" ", strip=True)
    return re.sub(r'\s+', ' ', text).strip()

async def download_document(url, download_dir, session):
    try:
        filename = url.split('/')[-1]
        filename = re.sub(r'[^\w\-\.]', '_', filename)
        file_path = os.path.join(download_dir, filename)

        if os.path.exists(file_path):
            print(f"Document already exists: {file_path}")
            return file_path

        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                content_disposition = response.headers.get('content-disposition')
                if content_disposition:
                    fname_match = re.search(r'filename="(.+)"', content_disposition)
                    if fname_match:
                        filename = fname_match.group(1)
                        filename = re.sub(r'[^\w\-\.]', '_', filename)
                        file_path = os.path.join(download_dir, filename)

                with open(file_path, 'wb') as f:
                    while True:
                        chunk = await response.content.read(8192)
                        if not chunk:
                            break
                        f.write(chunk)
                return file_path
            else:
                print(f"Failed to download {url}: Status {response.status}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    return None

def is_valid_url(url, base_domain):
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return False
    return parsed.netloc == base_domain or parsed.netloc.endswith('.' + base_domain)