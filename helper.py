import os
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def create_folder(foldername):
    """
    Create a new folder with the given foldername if it doesn't already exist.

    Args:
        foldername (str): The name of the folder to create.

    Returns:
        None
    """

    folder_path = os.path.join(os.getcwd(), foldername)

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def append_data_to_json_file(new_items, filename):
    """
    Append new_items to a JSON file with the given filename. If the file doesn't exist,
    it will be created and data will be written as the initial content.

    Args:
        new_items (list): The data to append to the JSON file.
        filename (str): The name of the JSON file.

    Returns:
        None
    """

    try:
        create_folder('output')
        filename = "output/"+filename
    
        with open(filename, 'r+') as file:
            # Load existing data
            existing_data = json.load(file)
            existing_data.append(new_items)
            file.seek(0)  # Move the file pointer to the beginning
            json.dump(existing_data, file, indent=4)

    except FileNotFoundError:
        # If the file doesn't exist, create and write new data
        with open(filename, 'w') as file:
            json.dump([new_items], file, indent=4)


def locate_element_by_css(driver, css_selector, wait=None, default_value=None):
    """
    Find and return the web element located by the given CSS selector.

    Args:
        driver (WebDriver): The WebDriver instance.
        css_selector (str): The CSS selector used to locate the web element.
        wait (int or None): The maximum time in seconds to wait for the element
                            to be visible (default: None).
        default_value (any): The value to return if the element is not found (default: None).

    Returns:
        WebElement or default_value: The web element located by the CSS selector, 
                                     or default_value if not found.

    """

    try:
        if wait is not None:
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, css_selector)))
            return element

        element = driver.find_element(By.CSS_SELECTOR, css_selector)
        return element

    except Exception as e:
        return default_value


def extract_opening_time(response):
    """
    Extracts the opening time from the given response string.

    Args:
        response (str): The response string containing opening time information.

    Returns:
        str: The extracted opening time, or an empty string if no opening time found.

    """

    if response == "":
        return response

    if '⋅' in response:
        response = response.split('⋅')[1]
        response = response.lower()

        if 'opens' in response:
            response = response.split('opens')[1]
            response = response.strip()

            if '\u202f' in response:
                response = response.replace('\u202f', ' ').upper()
    
        return response
