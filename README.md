# Google Maps Scraper

This project is a web scraper designed to extract data from Google Maps. It automates the process of searching for specific information and capturing details from individual blocks on the search results page. The scraped data is then stored in a JSON file.

## Usage

1. Open the `main.py` file in your preferred Python IDE or editor.

2. Locate the `scrape_website` function in `main.py`. This is the main entry point for running the scraper.

3. Ensure that you have a valid internet connection.

4. Customize the scraper parameters:
- Update the input field to specify the data you want to scrape.

5. Run the `scrape_website` function to initiate the scraping process.

6. Wait for the scraper to navigate to the Google Maps search page, enter the search query, and retrieve the search results.

7. The blocks on the search results page will be passed to the block parser, which extracts the required details such as Restaurant name, Location of restaurant (URL), Rating, Number of reviews, Address , Website ,Phone number,Category and Opening hours.

8. The extracted data will be stored in a JSON file for further analysis or use.
