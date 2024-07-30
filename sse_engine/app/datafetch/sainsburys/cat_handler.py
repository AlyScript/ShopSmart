from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import time
from tqdm import tqdm

import sainsburys.page_composer as page_composer
import mysql.connector

# eg link: '/gol-ui/groceries/pet/special-offers/c:1020463'

def get_num_pages(driver: webdriver.Chrome, cat_href: str):
    link = 'https://www.sainsburys.co.uk{0}'.format(cat_href)
    driver.get(link)
    time.sleep(5) # Let the page load
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    len_list = soup.find('ul', class_='ln-c-pagination__list')
    len_nums_list = len_list.find_all('a', class_='ln-c-pagination__link')
    
    for len_num in reversed(len_nums_list):
         val = len_num.get_text()
         try:
             val = int(val)
             return val
         except:
                pass
    return -1 ## ERRANEOUS CASE

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
    
    page_span = get_num_pages(driver=driver, cat_href=cat_href)
    formed_items = list()
    page_range = range(1, page_span + 1)
    
    for i in tqdm(page_range, desc='Building Category'):
        formed_href = cat_href + f'/opt/page:{i}'
        loc_items = page_composer.build_page(driver=driver, cat_href=formed_href)
        formed_items.extend(loc_items)
        
    for i in tqdm(range(len(formed_items)), desc='Committing to SQL...'):
        formed_items[i].commit_to_sql(mydb=mydb)
    
    return formed_items

# res = build_category(cat_href='/gol-ui/groceries/fruit-and-vegetables/flowers-and-plants/c:1020005')
# print(len(res))
