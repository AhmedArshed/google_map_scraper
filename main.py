import logging
import chromedriver_autoinstaller

from selenium import webdriver
from time import sleep

from helper import append_data_to_json_file
from parse_google_map import *

from constants import WEBSITE_URL, SEARCH_STRING, NUMBER_TO_SCRAPE


logging.basicConfig(
    level=logging.DEBUG,

    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log'  # Specified log file name
)


def parse_blocks(driver, block_details):
    """
    Parses the block details to extract information for each restaurant block.

    Args:
        block_details (list): List of block elements containing restaurant details.
        driver (WebDriver): WebDriver instance.

    Returns:
        None

    Description:
        This function iterates over the block details and extracts relevant information for each restaurant block.
        The function collects the following details for each restaurant block:
        - Restaurant name
        - Location of restaurant (URL)
        - Rating
        - Number of reviews
        - Address
        - Website
        - Phone number
        - Category
        - Opening hours

        The function utilizes various helper functions to extract specific information from each block element.
        It scrolls to each block element, clicks on it to expand the details, and retrieves the required information.
        The extracted information is then appended to a JSON file named "restaurant.json".

        Note:
        - The NUMBER_TO_SCRAPE constant determines the maximum number of restaurants to scrape.
        - The sleep() function is used to introduce delays for proper page loading and element visibility.

    """
    block_start = 0
    block_count = 0
    sleep(2)
    while block_count != NUMBER_TO_SCRAPE:
        for block in block_details[block_start:]:
            block_info = get_block_info(block)
            if block_info is None:
                continue
    
            restaurant_name = get_restaurant_name(block_info)
            restaurant_link = get_restaurant_link(block_info)
            click_to_view_restaurant_details(driver, block)
            rating, number_of_reviews = get_rating_and_number_of_reviews(driver)
            category = get_category(driver)
            website = get_website(driver)
            address = get_address(driver)
            phone_no = get_phone_no(driver)
            hours = get_opening_hours(driver)

            data_object = {
                "restaurant_name": restaurant_name,
                "google_map_link_for_restaurant": restaurant_link,
                "rating": rating,
                "number_of_reviews": number_of_reviews,
                "address": address,
                "website": website,
                "phone": phone_no,
                "category": category,
                "Opening_hours": hours
            }
            append_data_to_json_file(data_object, "restaurant.json")
            block_count += 1

        block_start = len(block_details)
        block_details = get_restaurant_block_elements(driver)


def scrape_website():
    """
    Scrapes the website by performing a search and parsing the restaurant blocks.

    Steps:
    1. Requests the website using the URL from the constants file.
    2. Sets an implicit wait of 10 seconds.
    3. Makes a search request using the search_string from the constants file.
    4. Retrieves the restaurant block elements from the page.
    5. Parses the block details.

    Returns:
        None

    """
    max_retries = 3
    retries = 0

    driver = webdriver.Chrome(chromedriver_autoinstaller.install())
    driver.implicitly_wait(10)

    while retries < max_retries:
        try:
            driver.get(WEBSITE_URL)
            driver.implicitly_wait(10)
            break           # Break out of the loop if the request is successful
        except Exception as e:
            logging.error("Request Failed: %s", str(e))
            retries += 1    # Increment the retries count
            sleep(1)        # Sleep for a short duration before the next retry

    if retries == max_retries:
        logging.error("Request failed after multiple retries!")
        return 

    make_search_request(driver, SEARCH_STRING)
    restaurant_block_elements = get_restaurant_block_elements(driver)
    parse_blocks(driver, restaurant_block_elements)


# Main function to scrape data from the website
scrape_website()
