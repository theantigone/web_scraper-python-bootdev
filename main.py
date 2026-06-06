import sys

from crawl import crawl_page


def main():
    print("Hello from web-scraper-python-bootdev!")

    args = sys.argv
    if len(args) < 2:
        print("no website provided")
        sys.exit(1)
    if len(args) > 2:
        print("too many arguments provided")
        sys.exit(1)

    base_url = args[1]

    print(f"starting crawl of: {base_url}...")

    try:
        html = crawl_page(base_url, base_url)
    except Exception as e:
        print(f"Error fetching HTML from {base_url}: {str(e)}")
        sys.exit(1)

    print("number of pages found:", len(html))
    for i, rich_page_data in enumerate(html, start=1):
        print("dictionary value", i, ":", rich_page_data)

    sys.exit(0)


if __name__ == "__main__":
    main()
