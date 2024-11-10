import os
import random
import time

from dotenv import load_dotenv
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.common.action_chains import ActionChains

from app.parsedpostdata import ParsedPostData
from app.exceptions import *
from app.config import *


def get_parsed_posts_data() -> list[ParsedPostData]:
    try:
        service = Service(executable_path=GeckoDriverManager().install())
        firefox_driver = webdriver.Firefox(service=service)
    except Exception:
        raise CreatingDriverInstanceError

    __log_into_patreon_account(firefox_driver)
    firefox_driver.get(NATALIEGOLD_URL)
    __filter_posts(firefox_driver)

    try:
        firefox_driver.find_element('xpath', '//div[text()="Clear filters"]')
    except Exception:
        raise FiltersAreNotAppliedError

    time.sleep(20)
    # load_more_button = firefox_driver.find_element('xpath', '(//div[contains(@style, "text-align")])/button')
    # click_element(firefox_driver, load_more_button)
    # time.sleep(20)

    post_cards = __get_all_post_cards(firefox_driver)

    for card in post_cards:
        parsed_post = __parse_post_card(firefox_driver, card)
        if parsed_post:
            print(parsed_post)


def __parse_post_card(firefox_driver: webdriver.Firefox, post_card: WebElement) -> ParsedPostData:
    try:
        post_link_element = post_card.find_element('xpath', '(.//span[@data-tag="post-title"])/a')
        post_href = post_link_element.get_attribute("href")

        youtube_link_element = post_card.find_element('xpath', './/div//p//a[contains(text(), "https://you")]')

        post_id = int(post_href.split('-')[-1])
        post_title = post_link_element.text.strip()
        post_url = f'{PATREON_URL.strip("/")}{post_href}'
        youtube_url = youtube_link_element.get_attribute('href') if youtube_link_element else None
    except Exception:
        return None

    return ParsedPostData(
        id=post_id,
        title=post_title,
        url=post_url,
        youtube_url=youtube_url
    )


def __get_all_post_cards(firefox_driver: webdriver.Firefox) -> list[WebElement]:
    time.sleep(15)
    all_post_cards = firefox_driver.find_elements('xpath', '//div[@data-tag="post-card"]')
    return all_post_cards


def __log_into_patreon_account(firefox_driver: webdriver.Firefox) -> None:
    account_email = os.environ['PATREON_EMAIL']
    account_password = os.environ['PATREON_PASSWORD']

    try:
        firefox_driver.get(PATREON_LOGIN_URL)
    except Exception:
        raise CantReachPatreonError
    wait_random_time()

    # entering email
    email_field = firefox_driver.find_element('xpath', '//input[@aria-label="Email"]')
    email_field.send_keys(account_email)
    continue_button = firefox_driver.find_element('xpath', '//button[@type="submit"]')
    click_element(firefox_driver, continue_button)
    wait_random_time()

    # entering password
    password_field = firefox_driver.find_element('xpath', '//input[@aria-label="Password"]')
    password_field.send_keys(account_password)
    click_element(firefox_driver, continue_button)
    wait_random_time()


def __filter_posts(firefox_driver: webdriver.Firefox) -> None:
    assert firefox_driver.current_url == NATALIEGOLD_URL, 'Trying to filter posts while no on the NatalieGold\'s page'

    # opening filter menu
    wait_random_time()
    post_type_menu = firefox_driver.find_element('xpath', '//button[@label="Post type"]')
    click_element(firefox_driver, post_type_menu)

    # post_type_menu.click()
    wait_random_time()

    # searching for Video filter
    content_type_buttons = firefox_driver.find_elements('xpath', '(//div[@role="dialog"])//button')
    for content_type_button in content_type_buttons:
        if 'Video' in content_type_button.text:
            click_element(firefox_driver, content_type_button)


def wait_random_time(min_sec=1, max_sec=5) -> None:
    time.sleep(random.randint(min_sec, max_sec))


def click_element(firefox_driver: webdriver.Firefox, element: WebElement) -> None:
    firefox_driver.execute_script("arguments[0].click();", element)


if __name__ == '__main__':
    load_dotenv()
    get_parsed_posts_data()
