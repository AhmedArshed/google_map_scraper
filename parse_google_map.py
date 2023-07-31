from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

from time import sleep
from helper import locate_element_by_css, extract_opening_time



def get_search_box_web_element(driver):
    """
    Find the input text area using the given webdriver.

    Args:
        driver (webdriver): The webdriver object for the web page.

    Returns:
        WebElement: The input text area web element.
    """

    input_text_area = locate_element_by_css(driver, 'input#searchboxinput')
    return input_text_area


def make_search_request(driver, search_string):
    """
    Find the input text area, If found, enter the given prompt text search
    and send ENTER button signal to make the search request.

    Args:
      driver(webdriver): Input Search web element where text will
                         be placed
      search_string(str): The prompt search for which we want results

    """

    input_text_area = locate_element_by_css(driver, 'input#searchboxinput')
    if input_text_area is not None:
        input_text_area.send_keys(search_string)
        input_text_area.send_keys(Keys.ENTER)


def get_restaurant_block_elements(driver):
    """
    Get the current listed blocks of restaurant elements from the web page.

    Args:
        driver (webdriver): The webdriver object for the web page.

    Returns:
        list: A list of WebElement objects representing the restaurant blocks.
    """

    restaurant_elements = driver.find_elements(
        By.CSS_SELECTOR, 'div[role=feed]  > div > div')
    return restaurant_elements


def get_block_info(driver):
    """
    Get the individual block information from the web page.

    Args:
        driver (webdriver): The webdriver object for the web page.

    Returns:
        WebElement: The individual block information web element from a tag.
    """

    try:
        block_info = driver.find_element(By.CSS_SELECTOR, 'a')
        return block_info
    except:
        return None


def get_restaurant_name(block_info):
    """
    Get the restaurant name from the block webelement.

    Args:
        block_info (WebElement): The block information web element that contains 
                                 data for an individual element.

    Returns:
        str: The name of the restaurant.
    """

    restaurant_name = block_info.get_attribute("aria-label")
    return restaurant_name


def get_restaurant_link(block_info):
    """
    Get the restaurant link from the block information.

    Args:
        block_info (WebElement): The block information web element that contains 
                                 data for an individual element.

    Returns:
        str: The google map link for the restaurant.
    """

    restaurant_link = block_info.get_attribute("href")
    return restaurant_link


def get_rating_and_number_of_reviews(driver):
    """
    Get the rating and number of reviews for a restaurant.

    Args:
        driver (webdriver): The webdriver object for the web page.

    Returns:
        float,int: The rating (float) and number of reviews (int).
    """

    rating_info = locate_element_by_css(driver, 'div.F7nice')
    if rating_info is not None:
        val = rating_info.text
    else:
        val = None

    if (val is None) or (val == ''):
        rating = None
        number_of_reviews = None
    else:
        rating = float(val[:3].replace(',', '.'))
        num = ''
        for c in val[3:]:
            if c.isdigit():
                num = num + c
        if len(num) > 0:
            number_of_reviews = int(num)
        else:
            number_of_reviews = None
    return rating, number_of_reviews


def get_category(driver):
    """
    Get the category of a restaurant.

    Args:
        driver (webdriver): The webdriver object for the web page.

    Returns:
        str: The category of the restaurant. If the category is not found or if 
            there is a StaleElementReferenceException,None will be returned.
    """

    category = locate_element_by_css(
        driver, "button[jsaction='pane.rating.category']", wait=10)
    if category is not None:
        try:
            category = category.text
        except StaleElementReferenceException:
            category = locate_element_by_css(
                driver, "button[jsaction='pane.rating.category']", wait=10)
            category = category.text

    return category


def get_website(driver):
    """
    Get the website of a restaurant.

    Args:
        driver (webdriver): The webdriver object for the web page.

    Returns:
        str: The website URL of the restaurant. If the website is not found or if 
        there is a StaleElementReferenceException,None will be returned.
    """

    website = locate_element_by_css(
        driver, "a[data-item-id='authority']", wait=10)
    if website is not None:
        try:
            website = website.text
        except StaleElementReferenceException:
            website = locate_element_by_css(
                driver, "a[data-item-id='authority']", wait=10)
            website = website.text
    return website


def get_address(driver):
    """
    Get the address of a restaurant.

    Args:
        driver (webdriver): The webdriver object for the web page.

    Returns:
        str: The address of the restaurant. If the address is not found or if 
        there is a StaleElementReferenceException,None will be returned.
    """

    address = locate_element_by_css(
        driver, "button[data-item-id='address']", wait=10)
    if address is not None:
        try:
            address = address.text
        except StaleElementReferenceException:
            address = locate_element_by_css(
                driver, "button[data-item-id='address']", wait=10)
            address = address.text
    return address


def get_phone_no(driver):
    """
    Get the phone number of a restaurant.

    Args:
        driver (webdriver): The webdriver object for the web page.

    Returns:
        str: The phone number of the restaurant. If the phone number is not found,
             an empty string will be returned.
    """

    phone_no = locate_element_by_css(driver, "button[data-item-id^='phone']")
    if phone_no is not None:
        try:
            phone = phone_no.get_attribute("data-item-id")
            if "phone:tel:" in phone:
                phone = phone.replace("phone:tel:", "")
        except:
            phone = ''
    else:
        phone = ''
    return phone


def get_opening_hours(driver):
    """
    Get the opening hours of a restaurant.

    Args:
        driver (webdriver): The webdriver object for the web page.

    Returns:
        str: The opening hours of the restaurant. If the opening hours are not found,
             an empty string will be returned.

    Raises:
        NoSuchElementException: If the opening hours element is not found using
                                both CSS selectors.
    """

    sleep(2)
    try:
        # First, try to find the opening hours element using the first CSS selector.
        hours_info = driver.find_element(
            By.CSS_SELECTOR, "div[role=region] button[data-item-id=oh]")
    except:
        # If the opening hours element is not found using the first CSS selector,
        # try finding it using the second CSS selector.
        hours_info = driver.find_element(
            By.CSS_SELECTOR, 'div[role=region] div[role=button]')
    try:
        hours = hours_info.find_elements(By.CSS_SELECTOR, 'span')[1].text
    except:
        hours = ""
    return extract_opening_time(hours)


def click_to_view_restaurant_details(driver, block):
    """
    Click on the restaurant block element to view details about the restaurant.

    Args:
        driver (webdriver): The webdriver object for the web page.
        block (WebElement): The block information web element that contains 
                            data for an individual element.
    """
    driver.execute_script('arguments[0].scrollIntoView(true);', block)
    sleep(1)
    block.click()
