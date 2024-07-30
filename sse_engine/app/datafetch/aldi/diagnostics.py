import aldi.locators as locators
import aldi.cat_handler as cat_handler

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import time

# Speed: Seconds per page
def calculate_scrape_time(verbose=False, est_page_speed=5.7):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")

    ### Set user agent to avoid bot detection
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    chrome_options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(options=chrome_options)

    page_num = 0
    overhead_time = 0

    start_time = time.time()
    extension_list = locators.collate_extension_list()
    end_time = time.time()
    overhead_time += end_time - start_time
    
    if verbose:
        print(f"Collating Extension List: {round(overhead_time, 4)} seconds.")
    
    for index, extension in enumerate(extension_list):
        if verbose:
            print(f'[{index+1}/{len(extension_list)}] {extension}')
        
        start_time = time.time() 
        len_span = cat_handler.get_num_pages(driver=driver, cat_href=extension)
        end_time = time.time()
        overhead_time += end_time - start_time
        
        page_num += len_span
        
    if verbose:
        print(f'Total number of pages: {page_num}')

    est_time = page_num * est_page_speed
    est_time += overhead_time
    
    if verbose:
        print("\n")
        print(f"Overhead Time: {round(overhead_time, 4)} seconds.")
        print(f'Estimated time to scrape: {est_time} seconds')
    
    return (est_time, page_num)

# Speed: Iterations per second
def calculate_sql_time(pages, verbose=False, speed=4.58):
    est_items = pages * 4 * 9
    est_items -= 15
    
    time_taken = est_items / speed
    if verbose:
        print(f"Est SQL Time for {est_items} items: {round(time_taken, 5)} seconds")
    
    return time_taken

print("STARTING DIAGNOSTICS...")
pages, time = calculate_scrape_time(verbose=True)
sql_time = calculate_sql_time(pages, verbose=True)

total_time = time + sql_time
print("\n")
print(f"Total EST TIME: {total_time} seconds.")