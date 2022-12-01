from os import getcwd, getenv, path
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver


class Requester:
    def __init__(self) -> None:
        firefox_options = FirefoxOptions()
        firefox_options.binary = getenv("FIREFOX_BINARY", "")
        self.browser = WebDriver(options=firefox_options)

    def __del__(self) -> None:
        self.browser.quit()

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.__del__()

    def request(self, method: str, url: str, data: dict = {}):
        inputs = []
        for key, value in data.items():
            inputs.append(f'<input type="text" name="{key}" value="{value}">')

        form = f"""
            <form action="{url}" method="{method}" id="formid">
                {inputs}
                <input type="submit" id="inputbox">
            </form>
        """

        self.browser.get(url)
        self.browser.execute_script(f"document.body.innerHTML = `{form}`")
        self.browser.find_element(By.ID, "inputbox").click()
