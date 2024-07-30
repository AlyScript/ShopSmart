from bs4 import BeautifulSoup
import re
import mysql.connector

class SainsburysItem:
    def __init__(self, product_div):
        
        ## NOTE: No Packsizes available from Sainsburys
        
        ## From Image Block...
        img_block = product_div.find('div', class_='pt__image-wrapper')
        self.image_href = img_block.find('img')['src']
        self.item_link = img_block.find('a')['href']
        
        ## From PT Wrapper (Inner)...
        data_block = product_div.find('div', class_='pt__wrapper-inner')
        self.item_title = data_block.find('a', class_='pt__link').get_text()
        
        ## Price...
        raw_price = data_block.find('span', class_='pt__cost__retail-price').get_text()
        if '£' in raw_price:
            self.price = float(raw_price[1:])
        elif 'p' in raw_price:
            self.price = float(raw_price[:-1]) / 100
        else:
            print(f"Unkown Price Value :: {raw_price}")
        
        self.price_per_unit_raw = data_block.find('span', class_='pt__cost__unit-price-per-measure').get_text()
        if '£' in self.price_per_unit_raw:
            price_united = re.search(r'£\d+\.\d+', self.price_per_unit_raw).group()[1:]
            price_united = float(price_united)
        else:
            price_united = re.search(r'\d{1,2}p', self.price_per_unit_raw).group()[:-1]
            price_united = float(price_united) / 100
            
        if ('/ 100g' in self.price_per_unit_raw) or ('/ 100ml' in self.price_per_unit_raw):
            self.price_per_kg = price_united * 10
        elif ('/ kg' in self.price_per_unit_raw) or ('/ ltr' in self.price_per_unit_raw):
            self.price_per_kg = price_united
        elif '75cl' in self.price_per_unit_raw:
            self.price_per_kg = float(price_united) * (1000 / 750)
        
        else:
            self.price_per_kg = 0.0
            print(f"Unkown unit: {self.price_per_unit_raw}")
        
        self.price_per_kg = round(self.price_per_kg, 2)
            
        ## Nectar Pricing...
        try:
            nectar_block = data_block.find('span', class_='pt__cost--price').get_text()
            if '£' in nectar_block:
                self.nectar_price = float(nectar_block[1:])
            elif 'p' in nectar_block:
                self.nectar_price = float(nectar_block[:-1]) / 100
            else:
                print(f"Unkown Nectar Price Value :: {nectar_block}")
            
            self.nectar_price_available = True
            self.nectar_price_per_kg = self.nectar_price * (1 / self.price) * self.price_per_kg
        
        except:
            self.nectar_price_available = False
            self.nectar_price = 0.0
            self.nectar_price_per_kg = 0.0
            
    def commit_to_sql(self, mydb):
        mycursor = mydb.cursor()
        
        full_sql = "INSERT INTO SainsburysItems_FULL " \
                   "(datetime, item_title, item_link, image_link, price, price_per_kg, nectar_price, nectar_price_per_kg) " \
                   "VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s); "
                   
        temp_sql = "INSERT INTO SainsburysItems_TEMP " \
                   "(datetime, item_title, item_link, image_link, price, price_per_kg, nectar_price, nectar_price_per_kg) " \
                   "VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s); "
        
        val = (self.item_title, self.item_link, self.image_href, self.price, self.price_per_kg, self.nectar_price, self.nectar_price_per_kg)
        mycursor.execute(full_sql, val)
        mycursor.execute(temp_sql, val)
        mydb.commit()

        return
        