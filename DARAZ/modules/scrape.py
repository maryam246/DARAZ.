from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import datetime
from colorama import Fore, Style  # Import colorama

class DarazScraper:
    def __init__(self, browser):
        self.browser = browser
        self.browser.implicitly_wait(10)  # Set implicit wait time to 10 seconds

    def scrape_product_data(self, url, min_discount_percentage, last_page_css_selector):
        try:
            self.browser.get(url)

            products_found = 0
            product_count = 1

            while True:
                title_css_selector = f"div.gridItem--Yd0sa:nth-child({product_count}) > div:nth-child(1) > a:nth-child(1) > div:nth-child(2) > div:nth-child(1)"
                link_css_selector = f"div.gridItem--Yd0sa:nth-child({product_count}) > div:nth-child(1) > a:nth-child(1)"
                actual_price_css_selector = f"div.gridItem--Yd0sa:nth-child({product_count}) > div:nth-child(1) > a:nth-child(1) > div:nth-child(2) > div:nth-child(4) > div:nth-child(1) > div:nth-child(2) > del:nth-child(1)"
                discount_price_css_selector = f"div.gridItem--Yd0sa:nth-child({product_count}) > div:nth-child(1) > a:nth-child(1) > div:nth-child(2) > div:nth-child(4) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2)"

                try:
                    title_element = self.browser.find_element(By.CSS_SELECTOR, title_css_selector)
                    link_element = self.browser.find_element(By.CSS_SELECTOR, link_css_selector)
                    actual_price_element = self.browser.find_element(By.CSS_SELECTOR, actual_price_css_selector)
                    discount_price_element = self.browser.find_element(By.CSS_SELECTOR, discount_price_css_selector)

                    title_text = title_element.text
                    link_text = link_element.get_attribute("href")
                    actual_price_text = actual_price_element.text
                    discount_price_text = discount_price_element.text
                    actual_price_value = float(actual_price_text.replace("Rs. ", "").replace(",", ""))
                    discount_price_value = float(discount_price_text.replace("Rs. ", "").replace(",", ""))
                    discount_percentage = int(((actual_price_value - discount_price_value) / actual_price_value) * 100)

                    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    if discount_percentage >= min_discount_percentage:
                        # Colorize the print statements
                        print(f"{Fore.GREEN}[DATETIME] {current_datetime}{Style.RESET_ALL}")
                        print(f"{Fore.CYAN}[TITLE] {title_text}{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}[URL] {link_text}{Style.RESET_ALL}")
                        print(f"{Fore.BLUE}[Actual Price] {actual_price_text}{Style.RESET_ALL}")
                        print(f"{Fore.RED}[Discount Price] Rs. {discount_price_text}{Style.RESET_ALL}")
                        print(f"{Fore.MAGENTA}[Discount Percentage] {discount_percentage}%{Style.RESET_ALL}\n")

                        with open('output.txt', 'a', encoding='utf-8') as fetch_data_file:
                            # Colorize the text in the output file
                            fetch_data_file.write(
                                f"[DATETIME] {current_datetime}\n"
                                f"[TITLE] {title_text}\n"
                                f"[URL] {link_text}\n"
                                f"[Actual Price] {actual_price_text}\n"
                                f"[Discount Price] Rs. {discount_price_text}\n"
                                f"[Discount Percentage] {discount_percentage}%\n\n"
                            )

                        products_found += 1

                    product_count += 1
                except Exception as e:
                    break

            # Check if the last page CSS selector is present
            if self.is_last_page(last_page_css_selector):
                print(f"{Fore.YELLOW}0 Product found on this Last page.{Style.RESET_ALL}")
                return False

            # Scroll down to load more products
            self.browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)

            print(f"{products_found} products found on this page.")

        except WebDriverException as wde:
            print(f"{Fore.RED}WebDriverException: {wde}{Style.RESET_ALL}")

        # Continue the loop
        return True

    def is_last_page(self, last_page_css_selector):
        try:
            # Check if the last page CSS selector is present on the current page
            return self.browser.find_element(By.CSS_SELECTOR, last_page_css_selector) is not None
        except NoSuchElementException:
            return False