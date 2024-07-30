from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import time

from tesco.tesco_item import TescoItem

def build_page(driver: webdriver.Chrome, cat_href: str):
    link = "https://www.tesco.com/{0}".format(cat_href)
    driver.get(link)
    time.sleep(5) # Let the page load
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    search_results = soup.find('ul', class_='product-list grid')
    item_blocks = search_results.findChildren('li', recursive=False)
    
    parsed_items = list()
    for item in item_blocks:
        main_div = item.find('div')
        for _ in range(3):
            main_div = main_div.find('div')
        
        parsed = TescoItem(product_div=main_div)
        parsed_items.append(parsed)
    
    return parsed_items
