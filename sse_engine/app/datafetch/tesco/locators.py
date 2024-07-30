from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import time

def collate_extension_list():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    
    ### Set user agent to avoid bot detection
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.tesco.com/groceries/en-GB/")
    
    # Give the page a chance to load; (replace w. EC in the future).
    time.sleep(5)
    
    extensions = []
    
    menu_finder = driver.find_element(By.XPATH, '//*[@id="groceries"]/div/div/ul')
    menu_list_items = menu_finder.find_elements(By.XPATH, './/li')
    
    for li_element in menu_list_items:
        li_element.click()
        
        _ = WebDriverWait(driver, 3).until(EC.presence_of_element_located((
            By.XPATH, './/ul/li[1]/a'
        )))
            
        main_subtitle = li_element.find_element(By.XPATH, './/ul/li[1]/a')
        href = main_subtitle.get_attribute('href')
        if 'easter' in href:
            print("Skipping Easter...")
            continue
        else:
            href = href.replace('https://www.tesco.com/', '')
            extensions.append(href)
            # print(href)
        
    driver.quit()
    return extensions

# res = collate_extension_list()
# print(res)
# print(len(res))
