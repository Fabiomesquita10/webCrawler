from bs4 import BeautifulSoup
from models.analytics_model import Price
import re
from playwright.sync_api import sync_playwright


def scrap_pc_diga_url(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        page = browser.new_page()
        page.goto(url)
        html_content = page.inner_html(
            "body"
        )  # Get the inner HTML of the <html> element
        return html_content
    

def pc_diga_price_scraper(html_content: str):
    soup = BeautifulSoup(html_content, "html.parser")
    price = {}
    newPrice = soup.find("div", class_="text-primary")

    if newPrice:
        price["newPrice"] = float(
            newPrice.text.strip().replace("€", "").replace(",", ".")
        )

    oldPrice = soup.find(
        "p", class_="text-xs tablet:text-sm font-black line-through pvpr-lh"
    )

    if oldPrice:
        price["oldPrice"] = float(
            oldPrice.text.strip().replace("€", "").replace(",", ".")
        )

    else:
        price["oldPrice"] = price["newPrice"]

    if not price:  # Retry if the prices are not found
        raise ValueError("Prices not found on the page")
    else:
        price["discount"] = price["oldPrice"] - price["newPrice"]

    return Price(**price)


def pc_diga_product_info_scraper(html_content: str):
    soup = BeautifulSoup(html_content, "html.parser")
    productName = soup.find("h1", class_="font-bold text-2xl")
    if productName:
        return productName.text.strip()
    return None


def pc_diga_promotion_date(html_content: str):
    soup = BeautifulSoup(html_content, "html.parser")
    priceValidity = soup.find("span", class_="text-sm")
    if priceValidity:
        dates = re.findall(r"\d{2}/\d{2}/\d{4}", priceValidity.text)
        return dates
    return None
