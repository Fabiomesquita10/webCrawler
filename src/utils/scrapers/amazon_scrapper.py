from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import re
import sys


def scrap(url: str, search_item: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=5000)
        page = browser.new_page()
        page.goto(url)
        search_input_selector = "#twotabsearchtextbox"
        page.fill(search_input_selector, search_item)
        search_button_selector = "#nav-search-submit-button"
        page.click(search_button_selector)

        html_content = page.inner_html("body")
        return html_content


def scrap_search_page(search_item: str) -> list:
    html_content = scrap("https://www.amazon.es/", search_item)

    soup = BeautifulSoup(html_content, "html.parser")
    search_results = soup.find_all(
        "div",
        class_="sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20",
    )

    items = []
    for index, data in enumerate(search_results):
        asin = data.get("data-uuid")

        title_element = data.find("h2").find("a").find("span")
        title = title_element.text.strip() if title_element else "N/A"

        price_element = data.find("span", class_="a-offscreen")
        price = price_element.text.strip() if price_element else "N/A"

        classification_element = data.find("span", class_="a-icon-alt")
        classification = (
            classification_element.text.strip() if classification_element else "N/A"
        )

        url_element = data.find("h2").find("a")
        url = "https://www.amazon.es" + url_element["href"] if url_element else "N/A"

        reviews_element = data.find("span", class_="a-size-base s-underline-text")
        reviews = reviews_element.text.strip() if reviews_element else "N/A"
        
        if index == 10: break
        items.append(
            {
                "uuid": asin,
                "title": title,
                "price": price,
                "classification": classification,
                "url": url,
                "number_reviews": reviews,
            }
        )

    return items
