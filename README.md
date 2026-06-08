# [Build a Web Scraper in Python](https://www.boot.dev/courses/build-web-scraper-python)

# prerequisites

- python 3.10+
- uv

# getting started

install the dependencies for this web crawler:

```sh
uv sync # recommended
```

alternatively, you can use the `pip` equivalent:

```sh
uv pip install -r requirements.txt
```

now, you can run the program

```sh
uv run main.py <base_url> <max_concurrency> <max_pages>
```

where:
- `<base_url>` is the website that you want to crawl
- `<max_concurrency>` is the limit of coroutines that you want to run (number of "agents" crawling, per se)
- `<max_pages>` is the limit on the number of pages that your crawler can crawl

for example:

```sh
# usage: uv run main.py URL max_concurrency max_pages
uv run main.py https://learnwebscraping.dev/practice/ecommerce/ 3 10
```

# dates

- start date: `5/26/2026`
- end date  : ``

=======

# running tests

to run all tests, run:

```sh
uv run -m unittest
```

for a verbose output (to see all of the tests individually in the shell):

```sh
uv run -m unittest -v
```

this command will execute all files that start with `test`
