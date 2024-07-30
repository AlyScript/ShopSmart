from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import time

from aldi.aldi_item import AldiItem

# eg link: '/en-GB/specially-selected?&page=1'

def build_page(driver: webdriver.Chrome, cat_href: str):
    link = "https://groceries.aldi.co.uk" + cat_href
    driver.get(link)
    
    # # Wait for the page to load
    # _ = WebDriverWait(driver, 3).until(
    #     EC.presence_of_element_located((By.ID, "vueSearchResults"))
    # )
    time.sleep(4)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    search_results = soup.find(id="vueSearchResults")
    row_block = search_results.find('div', class_='row')
    item_blocks = row_block.find_all('div', attrs={'data-qa' : 'search-results'})
    
    ### Website Update Detection. Exp. 36 elements.
    if len(item_blocks) != 36:
        print(f"WEB Changed! Unexpected number pyof items found on page_composer.py... detected len: {len(item_blocks)}")
    
    parsed_items = list()
    for item in item_blocks:
        parsed = AldiItem(product_div=item)
        parsed_items.append(parsed)
    
    return parsed_items

# print(len(build_page('/en-GB/specially-selected?&page=1')))
