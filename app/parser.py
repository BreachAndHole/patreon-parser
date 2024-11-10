import os
import random
import time

from typing import Optional

from dotenv import load_dotenv
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.remote.webdriver import WebElement

from app.parsedpostdata import ParsedPostData
from app.exceptions import *
from app.config import *
from app import queries


def get_parsed_posts_data() -> Optional[list[ParsedPostData]]:
    driver = __get_firefox_driver()

    try:
        __log_into_patreon_account(driver)
        print('Logged in successfully')
    except Exception:
        raise CantLogInError

    print('Opening NatalieGold posts page')
    driver.get(NATALIEGOLD_URL)

    try:
        __show_only_video_posts(driver)
        wait_random_time(10, 15)
        print('Video filtered successfully')
    except Exception:
        raise CantFiterVideoError

    # TODO: загрудзить последний id поста из файла
    # last_saved_id = 112852421
    last_saved_id = 110643256

    print('Getting last patreon post id')
    last_post_id = __get_last_post_id(driver)
    print(f'Last post ID: {last_post_id}')

    if last_post_id <= last_saved_id:
        print('No new posts')
        return None

    while not __is_post_on_current_page(driver, last_saved_id):
        print(f'Loading more posts to find post with ID {last_saved_id}')
        __load_another_page(driver, delay_sec=15)

    print(f'Post with id {last_saved_id} was found')
    post_cards = __get_all_post_cards(driver)
    parsed_posts = parse_post_cards(driver, post_cards)

    print('-' * 40)
    print(f'{len(parsed_posts)=}')
    [print(post) for post in parsed_posts]


def __get_firefox_driver() -> webdriver.Firefox:
    try:
        print('Creating Firefox instance')
        service = Service(executable_path=GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service)
    except Exception:
        raise CreatingDriverInstanceError
    return driver


def parse_post_cards(driver: webdriver.Firefox, post_cards: list[WebElement]) -> list[ParsedPostData]:
    print('Parsing post cards')
    parsed_posts: list[ParsedPostData] = []
    for i, card in enumerate(post_cards, 1):
        print(f'parsing {i}/{len(post_cards)} post card')
        parsed_post = __parse_post_card(card)

        if parsed_post:
            parsed_posts.append(parsed_post)
    return parsed_posts


def __load_another_page(driver: webdriver.Firefox, delay_sec=0) -> None:
    load_more_button = driver.find_element('xpath', queries.LOAD_MORE_POSTS_BUTTON_XPATH)
    click_on_element(driver, load_more_button)
    time.sleep(delay_sec)


def __is_post_on_current_page(driver: webdriver.Firefox, post_id: int) -> bool:
    print(f'Checking if post with ID {post_id} is on current page')
    search_post_by_id_xpath = f'//a[contains(@href, {post_id})]'
    matching_elements = driver.find_elements('xpath', search_post_by_id_xpath)
    print(f'{len(matching_elements)=}')
    return bool(len(matching_elements))


def __scroll_page_to_the_end(firefox_driver: webdriver.Firefox) -> None:
    page = 1
    while True:
        page += 1
        print(f'Loading page {page}')
        time.sleep(15)
        try:
            load_more_button = firefox_driver.find_element('xpath', '(//div[contains(@style, "text-align")])/button')
            click_on_element(firefox_driver, load_more_button)
        except Exception:
            print(f'Can\'t find a button on page {page}')
            break


def __parse_post_card(post_card: WebElement) -> Optional[ParsedPostData]:
    try:
        print('Fetching post URL')
        post_url_and_title_element = post_card.find_element('xpath', queries.POST_URL_XPATH)
        post_href = post_url_and_title_element.get_attribute("href")
        post_full_url = f'{PATREON_URL.strip("/")}{post_href}'

        print('Fetching post id')
        post_id = int(post_href.split('-')[-1])

        print('Fetching YouTube URL')
        youtube_link_element = post_card.find_element('xpath', queries.YOUTUBE_URL_XPATH)
        youtube_url = youtube_link_element.get_attribute('href')

        post_title = post_url_and_title_element.text.strip()
    except Exception:
        return None

    return ParsedPostData(
        id=post_id,
        title=post_title,
        url=post_full_url,
        youtube_url=youtube_url
    )


def __get_all_post_cards(driver: webdriver.Firefox) -> list[WebElement]:
    print('Getting all post cards')
    all_post_cards = driver.find_elements('xpath', queries.POST_CARD_XPATH)
    print(f'{len(all_post_cards)} post cards was fetched')
    return all_post_cards


def __log_into_patreon_account(driver: webdriver.Firefox) -> None:
    print('Getting login credentials')
    account_email = os.environ['PATREON_EMAIL']
    account_password = os.environ['PATREON_PASSWORD']

    try:
        print(f'Opening patreon login page ({PATREON_LOGIN_URL})')
        driver.get(PATREON_LOGIN_URL)
    except Exception:
        raise CantReachPatreonError
    wait_random_time()

    # entering email
    print('Entering Email')
    email_field = driver.find_element('xpath', queries.EMAIL_FIELD_XPATH)
    email_field.send_keys(account_email)
    print('Confirming Email')
    continue_button = driver.find_element('xpath', queries.CONTINUE_LOGIN_BUTTON_XPATH)
    click_on_element(driver, continue_button)
    wait_random_time()

    # entering password
    print('Entering password')
    password_field = driver.find_element('xpath', queries.PASSWORD_FIELD_XPATH)
    password_field.send_keys(account_password)
    print('Confirming password')
    click_on_element(driver, continue_button)
    wait_random_time()


def __show_only_video_posts(driver: webdriver.Firefox) -> None:
    assert driver.current_url == NATALIEGOLD_URL, 'Trying to filter posts while no on the NatalieGold\'s page'
    print('Applying only Video filter')
    # opening filter menu
    print('Opening filter drop-down menu')
    wait_random_time()
    post_type_menu = driver.find_element('xpath', queries.CONTENT_TYPE_FILTER_XPATH)
    click_on_element(driver, post_type_menu)

    # searching for Video filter
    wait_random_time()
    print('Searching for Video button')
    content_type_buttons = driver.find_elements('xpath', queries.CONTENT_TYPE_BUTTONS_XPATH)
    for button in reversed(content_type_buttons):
        if 'Video' in button.text:
            click_on_element(driver, button)
            break


def __filter_old_to_new_posts(driver: webdriver.Firefox) -> None:
    wait_random_time()
    assert driver.current_url == NATALIEGOLD_URL, 'Trying to filter posts while no on the NatalieGold\'s page'
    sort_button_element = driver.find_element('xpath', '//button[@aria-label="Sort posts by age"]')
    click_on_element(driver, sort_button_element)

    wait_random_time()
    sorting_list = driver.find_elements('xpath', '//ul')[-1]
    old_to_new_button = sorting_list.find_elements('xpath', './li')[-1].find_element('xpath', './a')
    click_on_element(driver, old_to_new_button)


def wait_random_time(min_sec=1, max_sec=5) -> None:
    time.sleep(random.randint(min_sec, max_sec))


def click_on_element(driver: webdriver.Firefox, element: WebElement) -> None:
    driver.execute_script("arguments[0].click();", element)


def __get_last_post_id(driver: webdriver.Firefox) -> int:
    post = driver.find_element('xpath', queries.POST_CARD_XPATH)
    post_href = post.find_element('xpath', queries.POST_URL_XPATH).get_attribute("href")
    post_id = int(post_href.split('-')[-1])
    return post_id


if __name__ == '__main__':
    load_dotenv()
    get_parsed_posts_data()
