from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import time

from sainsburys.sainsburys_item import SainsburysItem

# from sainsburys.sainsburys_item import SainsburysItem

def build_page(driver: webdriver.Chrome, cat_href: str):
    link = "https://www.sainsburys.co.uk{0}".format(cat_href)
    driver.get(link)
    time.sleep(5) # Let the page load
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    search_results = soup.find('ul', class_='ln-o-grid ln-o-grid--matrix ln-o-grid--equal-height')
    item_blocks = search_results.find_all('li', class_='pt-grid-item ln-o-grid__item ln-u-6/12@xs ln-u-1/3@sm ln-u-3/12@md ln-u-2/12@xl')
    
    parsed_items = list()
    for item in item_blocks:
        parsed = SainsburysItem(product_div=item)
        parsed_items.append(parsed)
    
    return parsed_items
