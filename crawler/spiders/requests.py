from os import getenv
from urllib.parse import urlparse
from scrapy.http import HtmlResponse, Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Spider
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from crawler.formextractors import FormExtractor

load_dotenv()


class RequestsSpider(Spider):
    name = "requests"
    target_url = getenv("TARGET_URL", "about:blank")
    allowed_domains = [urlparse(target_url).hostname]
    link_extractor = LinkExtractor(
        allow=f"{target_url}/.*",
        unique=False,
    )
    form_extractor = FormExtractor()

    def start_requests(self):
        # self._login()
        yield Request(self.target_url, callback=self.parse)

    def parse(self, response: HtmlResponse):
        print(self.form_extractor.extract_forms(response))
        # for link in self.link_extractor.extract_links(response):
        #     yield Request(link.url, callback=self.parse)

    def _login(self):
        login_url = f"{self.target_url}#/login"
        email = getenv("JUICE_SHOP_EMAIL")
        password = getenv("JUICE_SHOP_PASSWORD")

        browser: WebDriver = self.crawler.browser
        browser.get(login_url)
        wait = WebDriverWait(browser, 10)

        close_welcome_dialog_button: WebElement = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".close-dialog"))
        )
        close_welcome_dialog_button.click()

        email_input: WebElement = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name=email]"))
        )
        email_input.send_keys(email)

        password_input: WebElement = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name=password]"))
        )
        password_input.send_keys(password)

        submit_button: WebElement = wait.until(
            EC.element_to_be_clickable((By.ID, "loginButton"))
        )
        submit_button.click()
