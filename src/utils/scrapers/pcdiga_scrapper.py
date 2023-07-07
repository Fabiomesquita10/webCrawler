from bs4 import BeautifulSoup
from models.price_model import Price
import re


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
