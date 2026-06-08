import asyncio
from typing import TypedDict
from urllib.parse import urljoin, urlparse

import aiohttp
import requests
from bs4 import BeautifulSoup, Tag


class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]


def normalize_url(url: str) -> str:
    parsed_url = urlparse(url)
    full_path = f"{parsed_url.netloc}{parsed_url.path}"
    full_path = full_path.rstrip("/")
    return full_path.lower()


def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    h_tag = soup.find("h1") or soup.find("h2")
    return h_tag.get_text(strip=True) if isinstance(h_tag, Tag) else ""


def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    main_section = soup.find("main")
    if isinstance(main_section, Tag):
        first_p = main_section.find("p")
    else:
        first_p = soup.find("p")

    return first_p.get_text(strip=True) if isinstance(first_p, Tag) else ""


def get_urls_from_html(html: str, base_url: str) -> list[str]:
    urls = []
    soup = BeautifulSoup(html, "html.parser")
    anchors = soup.find_all("a")

    for anchor in anchors:
        if not isinstance(anchor, Tag):
            continue
        href = anchor.get("href")
        if isinstance(href, str) and href:
            try:
                absolute_url = urljoin(base_url, href)
                urls.append(absolute_url)
            except Exception as e:
                print(f"{str(e)}: {href}")

    return urls


def get_images_from_html(html: str, base_url: str) -> list[str]:
    image_urls = []
    soup = BeautifulSoup(html, "html.parser")
    images = soup.find_all("img")

    for img in images:
        if not isinstance(img, Tag):
            continue
        src = img.get("src")
        if isinstance(src, str) and src:
            try:
                absolute_url = urljoin(base_url, src)
                image_urls.append(absolute_url)
            except Exception as e:
                print(f"{str(e)}: {src}")

    return image_urls


def extract_page_data(html: str, page_url: str) -> PageData:
    return {
        "url": page_url,
        "heading": get_heading_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url),
    }


class AsyncCrawler:
    def __init__(
        self,
        base_url: str,
        page_data: dict[str],
        max_concurrency: int,
    ):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.page_data = page_data
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if normalized_url not in self.page_data:
                self.page_data[normalized_url] = 0
                return True
            return False

    async def get_html(self, url: str) -> str:
        async with self.session.get(url) as response:
            if response.status > 399:
                raise Exception(f"got HTTP error: {response.status} {response.reason}")

            content_type = response.headers.get("content-type", "")
            if "text/html" not in content_type:
                raise Exception(f"got non-HTML response: {content_type}")

            return await response.text()

    async def crawl_page(self, current_url: str | None = None):
        if current_url is None:
            current_url = self.base_url

        base_url_obj = urlparse(self.base_url)
        current_url_obj = urlparse(current_url)
        if current_url_obj.netloc != base_url_obj.netloc:
            return self.page_data

        normalized_url = normalize_url(current_url)

        check = await self.add_page_visit(normalized_url)

        # if normalized_url in page_data:
        #    return page_data
        if not check:
            return self.page_data

        tasks = []
        print(f"crawling {current_url}")
        async with self.semaphore:
            html = await self.get_html(current_url)
            if html is None:
                return self.page_data

            page_info = extract_page_data(html, current_url)
            async with self.lock:
                self.page_data[normalized_url] = page_info

            next_urls = get_urls_from_html(html, self.base_url)
            for next_url in next_urls:
                tasks.append(asyncio.create_task(self.crawl_page(next_url)))

        await asyncio.gather(*tasks)

        return self.page_data

    async def crawl(self):
        return await self.crawl_page(self.base_url)


async def crawl_site_async(base_url):
    urls = {}
    urls[normalize_url(base_url)] = 0
    async with AsyncCrawler(base_url, urls, 5) as crawler:
        return await crawler.crawl()
