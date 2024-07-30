from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import time
from tqdm import tqdm

import aldi.page_composer as page_composer
import mysql.connector

# eg link: '/en-GB/specially-selected'
# exp form for composer: '/en-GB/specially-selected?&page=1'

def get_num_pages(driver: webdriver.Chrome, cat_href: str):
    link = 'https://groceries.aldi.co.uk' + cat_href + '?&page=1'
    driver.get(link)
    time.sleep(2) # Let the page load
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    len_span = soup.find('span', class_='d-flex-inline pt-2').get_text()
    len_span = int(len_span.replace(' ', '').replace('of', ''))

    return len_span

def build_category(cat_href: str):
    
    mydb = mysql.connector.connect(
        host='dbhost.cs.man.ac.uk',
        user="h34567pv",
        password="Kekes-Database_Army+707++",
        database="2023_comp10120_z8"
    )
    
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    
    ### Set user agent to avoid bot detection
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(options=chrome_options)
    
    len_span = get_num_pages(driver=driver, cat_href=cat_href)
    formed_items = list()
    page_range = range(1, len_span + 1)
    
    for i in tqdm(page_range, desc='Building Category'):
        formed_href = cat_href + f'?&page={i}'
        loc_items = page_composer.build_page(driver=driver, cat_href=formed_href)
        formed_items.extend(loc_items)
        # print(f"Page {i} of {len_span} complete.")
        
    for i in tqdm(range(len(formed_items)), desc='Committing to SQL...'):
        formed_items[i].commit_to_sql(mydb=mydb)
        
    return formed_items
            
# print(len(build_category('/en-GB/specially-selected')))
