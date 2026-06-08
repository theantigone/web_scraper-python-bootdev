import json
from typing import TypedDict


class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]


def write_json_report(page_data: dict[str, PageData], filename="report.json"):
    pages = sorted(page_data.values(), key=lambda p: p["url"])
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(pages, f, indent=2)
