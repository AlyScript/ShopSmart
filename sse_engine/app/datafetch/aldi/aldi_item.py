from bs4 import BeautifulSoup
import re
import mysql.connector

class AldiItem:
    def __init__(self, product_div):
        self.image_href = product_div.find('img', class_='img-fluid product-image')['src']
        self.pack_size = product_div.find('div', class_='text-gray-small').get_text()
        self.item_title = product_div.find('a', class_='p text-default-font').get_text()
        
        ### Price
        span_h4 = product_div.find('span', class_='h4')
        self.price = float(span_h4.find('span').get_text()[1:])
        
        self.item_link = product_div.find('a', class_='p text-default-font')['href']
        
        ### Price per kg parsing
        small_block = product_div.find('small', class_='mr-1 text-gray-small')
        if small_block is None:
            small_block = product_div.find('small', class_='mr-1 text-gray-small text-danger')
            self.price_per_unit_raw = small_block.find('span').get_text()
        else:
            self.price_per_unit_raw = small_block.find('span').get_text()
        
        # price_united = re.search(r'£\d+\.\d+', self.price_per_unit_raw).group()[1:]
        if '£' in self.price_per_unit_raw:
            price_united = re.search(r'£\d+\.\d+', self.price_per_unit_raw).group()[1:]
        else:
            price_united = re.search(r'\d+\.\d+p', self.price_per_unit_raw).group()[:-1]    
        
        # try:
        #     price_united = re.search(r'£\d+\.\d+', self.price_per_unit_raw).group()[1:]
        # except Exception as e:
        #     print(e)
        #     print(self.price_per_unit_raw)
        
        if 'kg' in self.price_per_unit_raw:
            self.price_per_kg = float(price_united)
        elif '100g' in self.price_per_unit_raw:
            self.price_per_kg = float(price_united) * 10
            
        elif '100ml' in self.price_per_unit_raw:
            self.price_per_kg = float(price_united) * 10   # Assume 100ml == 100g ie. 1000ml == 1kg
        elif 'per litre' in self.price_per_unit_raw:
            self.price_per_kg = float(price_united)
        elif '75cl' in self.price_per_unit_raw:
            self.price_per_kg = float(price_united) * (1000 / 750)
        
        else:
            self.price_per_kg = 0.0
            print(f"Unkown unit: {self.price_per_unit_raw}")
        
        self.price_per_kg = round(self.price_per_kg, 2)
        
    def commit_to_sql(self, mydb):
        mycursor = mydb.cursor()
        
        full_sql = "INSERT INTO AldiItems_FULL " \
                   "(datetime, item_title, item_link, image_link, price, price_per_kg) " \
                   "VALUES (NOW(), %s, %s, %s, %s, %s); "
                   
        temp_sql = "INSERT INTO AldiItems_TEMP " \
                   "(datetime, item_title, item_link, image_link, price, price_per_kg) " \
                   "VALUES (NOW(), %s, %s, %s, %s, %s); "
        
        val = (self.item_title, self.item_link, self.image_href, self.price, self.price_per_kg)
        mycursor.execute(full_sql, val)
        mycursor.execute(temp_sql, val)
        mydb.commit()

        return
        