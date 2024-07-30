from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

# Compile a list of all of the url extensions in the header bar...
# Base URL: https://groceries.aldi.co.uk/en-GB/

def collate_extension_list():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    
    ### Set user agent to avoid bot detection
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://groceries.aldi.co.uk/en-GB/")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    level_two = soup.find(id='level2')
    midlevels = level_two.find_all('li', class_='submenu mb-0 mb-submenu level3Menu')
    extensions = []
    
    for midlevel in midlevels:
        dropdowns = midlevel.find_all('a', class_='dropdown-item')
        for dropdown in dropdowns:
            if 'SHOP ALL' in dropdown.get_text():
                href = dropdown['href']
                href = href.split('?')[0]
                extensions.append(href)
    
    driver.quit()
    return extensions

# print(collate_extension_list())
