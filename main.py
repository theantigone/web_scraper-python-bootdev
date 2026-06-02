import sys


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


if __name__ == "__main__":
    main()
