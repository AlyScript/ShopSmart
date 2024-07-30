from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import time

# Compile a list of all of the url extensions in the header bar...
# Navigate each sub menu - if there is an ALL, select. If not, Dive deeper and repeat logic.
# Base URL: https://www.sainsburys.co.uk/shop/gb/groceries
# Sub Link Level 1:'https://www.sainsburys.co.uk/shop/gb/groceries/new---trending?fromMegaNav=1'
# Final HREF Form: "/gol-ui/groceries/baby-and-toddler/accessories/all-accessories/c:1018673"

def collate_extension_list():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    
    ### Set user agent to avoid bot detection
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.sainsburys.co.uk/shop/gb/groceries")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    extensions = []
    main_extensions = []
    
    mega_finder = soup.find(id='megaNavLevelOne')
    mega_finder = mega_finder.find_all('a', class_='megaNavLink')
    for item in mega_finder:
        if 'fromMegaNav=1' in item['href']:
            main_extensions.append(item['href'])
    
    for main_extension in main_extensions:
        try:
            driver.get(main_extension)
            time.sleep(5)
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            sub_list = soup.find('ul', class_='browse-pill-list browse-pill-list__disable-scrollbars')
            
            # print(sub_list)
            # print(len(sub_list))

            list_elements = sub_list.find_all('li')
            for list_element in list_elements:
                href = list_element.find('a')['href']
                extensions.append(href)
        except:
            print(f"Exception Caught !!! ---  Extension Type: {0}".format(main_extension))
    
    driver.quit()
    return extensions

# res = collate_extension_list()
# print(res)
# print(len(res))
