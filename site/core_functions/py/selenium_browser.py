"""Helper function to create a selenium web browser."""
from typing import Union
from base64 import b64encode
from selenium import webdriver
from selenium.common import exceptions
from webdriver_manager.chrome import ChromeDriverManager


def selenium_browser():
    """Helper function to create a selenium web browser."""

    try:
        browser = webdriver.Chrome('chromedriver.exe')
    except exceptions.WebDriverException:
        opt = webdriver.ChromeOptions()
        opt.add_argument('--disable-extensions')
        opt.add_argument('--disable-gpu')
        opt.add_argument("--disable-dev-shm-usage")
        opt.add_argument("--no-sandbox")
        opt.add_argument("--headless")
        opt.add_argument("--disable-web-security")
        opt.add_argument("--allow-running-insecure-content")

        browser = webdriver.Chrome(
            ChromeDriverManager().install(),
            options=opt
        )

    browser.set_window_size(1440, 900)

    return browser


def parse_response(response: Union[bytes, str]) -> selenium_browser:
    """Parse the response returned from a browser."""
    response_encoded = b64encode(str(response).encode('utf-8')).decode()
    driver = selenium_browser()
    driver.get('data:text/html;base64,{}'.format(response_encoded))
    return driver
