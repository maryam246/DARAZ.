from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from modules import clrscr
from modules import banner
from modules.scrape import DarazScraper
import json
from colorama import init, Fore, Style
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import datetime
from urllib.parse import urlparse, urlunparse

# Initialize colorama
init()

clrscr.clear_screen()
banner.Banner()
# Ask for the minimum discount percentage
percent = int(input(f"{Fore.GREEN}Enter Minimum Discount Percentage [1-100]: {Style.RESET_ALL}"))
bswr = input(f"{Fore.RED}Do you want to search in browser{Style.RESET_ALL} {Fore.GREEN}(It can take more time){Style.RESET_ALL} [Y/n] : ")

if bswr == "Y" or bswr == "y" :
    browser_open = 1
elif bswr == "N" or bswr == "n" :
    browser_open = 0
else:
    print(f'{colors.bcolors.RED}Invalid input try again{colors.bcolors.ENDC}')
    exit()


# Initialize browser
options = Options()
options.headless = False  # Set to True if you want the browser to run in headless mode
browser = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
browser.minimize_window()


def update_urls(url):
    parsed_url = urlparse(url)

    # Check if the URL has query parameters
    if parsed_url.query:
        # Remove existing query parameters
        updated_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', ''))
    else:
        # If there are no query parameters, keep the original URL
        updated_url = url

    # Append '?page=' to the updated URL
    updated_url += '?page='

    return updated_url

# Scraping categories
categories_data = {}
try:
    browser.get("https://www.daraz.pk")

    # Wait for the menu to load
    menu_element = WebDriverWait(browser, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div/div/div/div/div/ul'))
    )

    parent_categories = menu_element.find_elements(By.XPATH, 'li')

    for parent_category_number, parent_category in enumerate(parent_categories, start=1):
        parent_category_name = parent_category.find_element(By.XPATH, 'a/span[2]').text
        # Click on the parent category
        parent_category.click()

        # Dynamically adjust the subcategories XPath based on the index of the parent category
        subcategories_xpath = f'/html/body/div[1]/div/div/div[2]/div/div/div/div/div/div/div/ul/ul[{parent_category_number}]/li'

        subcategory_items = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, subcategories_xpath))
        )

        subcategories_data = {}

        for index, subcategory_item in enumerate(subcategory_items, start=1):
            subcategory_name = subcategory_item.find_element(By.XPATH, 'a/span').text
            subcategory_url = subcategory_item.find_element(By.XPATH, 'a').get_attribute('href')

            # Update the subcategory URLs
            updated_subcategory_url = update_urls(subcategory_url)

            subcategories_data[subcategory_name] = updated_subcategory_url

        categories_data[parent_category_name] = subcategories_data

except Exception as e:
    print(f"An error occurred: {e}")

    # Store the data in a JSON file
with open('categories_data.json', 'w') as json_file:
    json.dump(categories_data, json_file, indent=4)

# Display parent categories to the user
print(f"\n{Fore.YELLOW} Select only one option from below list: {Style.RESET_ALL}")
for index, (parent_category_name, _) in enumerate(categories_data.items(), start=1):
    print(f"{Fore.CYAN}[{index}] {parent_category_name}{Style.RESET_ALL}")

# Prompt user for parent category selection
selected_parent_index = int(input(f"\n{Fore.WHITE} Enter Number: {Style.RESET_ALL} ")) - 1
selected_parent_category = list(categories_data.keys())[selected_parent_index]

# Display subcategories to the user based on the selected parent category
print(f"\n{Fore.YELLOW} Select only one option from below list: {selected_parent_category}:{Style.RESET_ALL}")
subcategories_data = categories_data[selected_parent_category]
for index, (subcategory_name, _) in enumerate(subcategories_data.items(), start=1):
    print(f"{Fore.MAGENTA}[{index}] {subcategory_name}{Style.RESET_ALL}")

# Prompt user for subcategory selection
selected_sub_index = int(input(f"\n{Fore.WHITE} Enter Number: {Style.RESET_ALL} ")) - 1
selected_subcategory_name = list(subcategories_data.keys())[selected_sub_index]
selected_subcategory_url = subcategories_data[selected_subcategory_name]


clrscr.clear_screen()
open('output.txt', 'w').close()
i = 1

last_page_css_selector = ".title--sUZjQ"

while True:
    url = selected_subcategory_url + str(i)
    print("<=================================================================================>".center(167))
    print(
        f'{Fore.RED}[{i}]{Style.RESET_ALL} Trying on --> {Fore.BLUE}{url}{Style.RESET_ALL}'.center(185))
    print("<=================================================================================>".center(167))
    print('\n')

    daraz_scraper = DarazScraper(browser)
    if not daraz_scraper.scrape_product_data(url, percent, last_page_css_selector):
        break  # Stop the loop if the last page is reached

    i += 1

# Close the browser after the loop
if browser is not None:
    browser.quit()