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
            
        html_content = page.inner_html(
            "body"
        )  
        return html_content



def scrap_search_page(search_item: str) -> list:
    html_content = scrap("https://www.amazon.es/", search_item)
    
    soup = BeautifulSoup(html_content, "html.parser")
    data = soup.find("div", class_="s-main-slot s-result-list s-search-results sg-row")
    print(data)
    return True