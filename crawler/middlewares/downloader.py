import asyncio
from os import getenv
import re
from scrapy import signals
from scrapy.http import HtmlResponse, Request as ScrapyRequest
from dotenv import load_dotenv
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import FirefoxOptions
from seleniumwire.webdriver import Firefox
from seleniumwire.request import Request as SeleniumWireRequest

from database.models import Request
from utils.format import formatCookie, formatPayload

load_dotenv()


TARGET_URL = getenv("TARGET_URL", "about:blank")
ACCEPTED_CONTENT_TYPE_PATTERN = re.compile(
    "|".join(
        [
            "(^application/.*json)",
            "(^application/.*xml)",
            "(^text/plain)",
            "(^text/html)",
        ]
    )
)


def interceptor(request: SeleniumWireRequest, response):
    content_type = response.headers.get("Content-Type", "")
    if (
        request.url.startswith(TARGET_URL)
        and ACCEPTED_CONTENT_TYPE_PATTERN.search(content_type) is not None
    ):
        request_model = Request(
            method="GET",
            url=request.url,
            headers=dict(request.headers),
            cookie=formatCookie(request.headers.get("cookie")),
            payload=formatPayload(request.body),
        )
        asyncio.run(request_model.insert())


def init_browser() -> WebDriver:
    firefox_options = FirefoxOptions()
    firefox_options.binary = getenv("FIREFOX_BINARY", "")
    browser = Firefox(options=firefox_options)
    browser.response_interceptor = interceptor

    return browser


class SeleniumDownloaderMiddleware:
    browser: WebDriver

    @classmethod
    def from_crawler(cls, crawler):
        if not hasattr(crawler, "browser"):
            crawler.browser = init_browser()
        s = cls(crawler.browser)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)

        return s

    def __init__(self, browser: WebDriver):
        self.browser = browser

    def process_request(self, request: ScrapyRequest, spider) -> HtmlResponse:
        self.browser.get(request.url)

        return HtmlResponse(
            url=request.url,
            body=str.encode(self.browser.page_source),
            encoding="utf-8",
            request=request,
        )

    def spider_closed(self):
        self.browser.quit()
