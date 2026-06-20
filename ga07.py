from collections import deque
from urllib.parse import urljoin, urldefrag, urlparse
import requests
from bs4 import BeautifulSoup
import re

START_URL = "https://sanand0.github.io/tdsdata/crawl_html/"

visited = set()
queue = deque([START_URL])

# record pages starting with g-r
g_to_r_pages = []

session = requests.Session()
session.headers.update({
    "User-Agent": "TDSCrawler/1.0"
})

def normalize(base_url, href):
    url = urljoin(base_url, href)
    url, _ = urldefrag(url)
    return url

while queue:
    url = queue.popleft()

    if url in visited:
        continue

    visited.add(url)

    try:
        r = session.get(url, timeout=10)
        r.raise_for_status()
    except Exception:
        continue

    # Check filename
    path = urlparse(url).path
    filename = path.split("/")[-1]

    # matches g.html ... r.html or g123.html ... r123.html
    if re.match(r"^[g-rG-R].*\.html?$", filename):
        g_to_r_pages.append(url)

    soup = BeautifulSoup(r.text, "html.parser")

    for a in soup.find_all("a", href=True):
        next_url = normalize(url, a["href"])

        if next_url.startswith(START_URL):
            if next_url not in visited:
                queue.append(next_url)

print("Pages starting with G-R:")
for page in sorted(g_to_r_pages):
    print(page)

print("\nTotal:", len(g_to_r_pages))