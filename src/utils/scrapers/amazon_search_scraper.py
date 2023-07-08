import logging
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

BASE_URL = "https://www.amazon.es"


class CustomException(Exception):
    pass


def wait_for_element(driver, locator, timeout=10):
    if not driver:
        raise ValueError("Invalid driver provided.")
    if not locator or not isinstance(locator, tuple) or len(locator) != 2:
        raise ValueError("Invalid locator provided.")

    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.presence_of_element_located(locator))
        return element
    except TimeoutException:
        raise TimeoutException("Element not found within the specified timeout.")


def extract_element_text(element):
    try:
        return element.text.strip()
    except AttributeError:
        return None


def scraped_data(data):
    try:
        uuid = data.get("data-uuid")

        title_element = data.find("h2").find("a").find("span")
        title = title_element.text.strip() if title_element else "N/A"

        price_element = data.find("span", class_="a-offscreen")
        price = price_element.text.strip() if price_element else "N/A"

        classification_element = data.find("span", class_="a-icon-alt")
        classification = (
            classification_element.text.strip() if classification_element else "N/A"
        )

        url_element = data.find("h2").find("a")
        url = url_element["href"] if url_element else "N/A"

        reviews_element = data.find("span", class_="a-size-base s-underline-text")
        reviews = reviews_element.text.strip() if reviews_element else "N/A"

        return {
            "uuid": uuid,
            "title": title,
            "price": price,
            "classification": classification,
            "url": url,
            "number_reviews": reviews,
        }
    except AttributeError as e:
        raise CustomException(f"Error scraping data: {e}")
    except Exception as e:
        logging.error(f"Error scraping data: {e}")
        return None


def scrap_search_page(search_item: str, num_items: int = 10) -> list:
    try:
        driver = webdriver.Chrome()
        driver.get("https://www.amazon.es/")
        search_box = wait_for_element(driver, (By.ID, "twotabsearchtextbox"))
        search_box.send_keys(search_item)
        search_button = wait_for_element(driver, (By.XPATH, "//input[@value='Ir']"))
        search_button.click()

        html_content = driver.page_source
        driver.quit()

        if html_content is None:
            return []

        soup = BeautifulSoup(html_content, "html.parser")
        search_results = soup.find_all(
            "div",
            class_="sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20",
        )

        items = []
        for index, data in enumerate(search_results):
            items.append(scraped_data(data))

            if index == num_items - 1:
                break

        return items
    except Exception as e:
        raise e
