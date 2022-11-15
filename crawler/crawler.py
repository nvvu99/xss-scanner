import gzip
import json
import os
import time
import re
from pprint import pprint

from seleniumwire import webdriver
from selenium.webdriver import FirefoxOptions

from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("URL", "about:blank")
ACCEPTED_CONTENT_TYPE_PATTERN = re.compile(
    "|".join(
        [
            "(^application\/.*json)",
            "(^application\/.*xml)",
            "(^text\/plain)",
            "(^text\/html)",
        ]
    )
)


def interceptor(request, response):
    content_type = response.headers.get("Content-Type", "")
    if (
        request.url.startswith(URL)
        and ACCEPTED_CONTENT_TYPE_PATTERN.search(content_type) is not None
    ):
        print(request.url)
        print(request.body.decode("utf-8"))

        try:
            response_body = response.body.decode("utf-8")
        except UnicodeDecodeError:
            response_body = gzip.decompress(response.body)

        print(response_body)
        print()


def main():
    firefox_options = FirefoxOptions()
    firefox_options.binary = os.getenv("FIREFOX_BINARY", "")
    with webdriver.Firefox(options=firefox_options) as driver:
        driver.response_interceptor = interceptor
        driver.get(URL)
        sleep_loop()


def sleep_loop() -> None:
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
