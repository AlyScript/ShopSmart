from bs4 import BeautifulSoup
import re

class TescoItem:
    def __init__(self, product_div):
        
        ## From Image Block...FIXED.
        # img_block = product_div.find('div', class_='product-image__container')
        self.image_href = product_div.find('img')['src']
        self.item_link = product_div.find('a')['href']
        
        ## From Product Details Wrapper (Inner)...
        data_block = product_div.find('div', class_='product-details--wrapper')
        self.item_title = data_block.find('a', class_='styled__Anchor-sc-1i711qa-0 hXcydL ddsweb-link__anchor').get_text()
        
        ## Price...
        raw_price = data_block.find('p', class_='styled__StyledHeading-sc-119w3hf-2 jWPEtj styled__Text-sc-8qlq5b-1 lnaeiZ beans-price__text').get_text()
        # styled__StyledHeading-sc-119w3hf-2 jWPEtj styled__Text-sc-8qlq5b-1 lnaeiZ beans-price__text
        if '£' in raw_price:
            self.price = float(raw_price[1:])
        elif 'p' in raw_price:
            self.price = float(raw_price[:-1]) / 100
        else:
            print(f"Unkown Price Value :: {raw_price}")
        
        self.price_per_unit_raw = data_block.find('p', class_='styled__StyledFootnote-sc-119w3hf-7 icrlVF styled__Subtext-sc-8qlq5b-2 bNJmdc beans-price__subtext').get_text()
        # styled__StyledFootnote-sc-119w3hf-7 icrlVF styled__Subtext-sc-8qlq5b-2 bNJmdc beans-price__subtext
        if '£' in self.price_per_unit_raw:
            price_united = re.search(r'£\d+\.\d+', self.price_per_unit_raw).group()[1:]
            price_united = float(price_united)
        else:
            price_united = re.search(r'\d{1,2}p', self.price_per_unit_raw).group()[:-1]
            price_united = float(price_united) / 100
            
        if ('/100g' in self.price_per_unit_raw) or ('/100ml' in self.price_per_unit_raw):
            self.price_per_kg = price_united * 10
        elif ('/kg' in self.price_per_unit_raw) or ('/litre' in self.price_per_unit_raw):
            self.price_per_kg = price_united
        elif '75cl' in self.price_per_unit_raw:
            self.price_per_kg = float(price_united) * (1000 / 750)
        
        else:
            self.price_per_kg = 0.0
            print(f"Unkown unit: {self.price_per_unit_raw}")
        
        self.price_per_kg = round(self.price_per_kg, 2)
            
        ## Clubcard Pricing...
        try:
            clubcard_block = data_block.find('span', class_='offer-text').get_text()
            if '£' in clubcard_block:
                self.clubcard_price = float(clubcard_block[1:])
            elif 'p' in clubcard_block:
                self.clubcard_price = float(clubcard_block[:-1]) / 100
            else:
                print(f"Unkown Nectar Price Value :: {clubcard_block}")
            
            self.clubcard_price_available = True
            self.clubcard_price_per_kg = self.clubcard_price * (1 / self.price) * self.price_per_kg
        
        except:
            self.clubcard_price_available = False
            self.clubcard_price = 0.0
            self.clubcard_price_per_kg = 0.0

    def commit_to_sql(self, mydb):
            mycursor = mydb.cursor()
            
            full_sql = "INSERT INTO TescoItems_FULL " \
                    "(datetime, item_title, item_link, image_link, price, price_per_kg, clubcard_price, clubcard_price_per_kg) " \
                    "VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s); "
                    
            temp_sql = "INSERT INTO TescoItems_TEMP " \
                    "(datetime, item_title, item_link, image_link, price, price_per_kg, clubcard_price, clubcard_price_per_kg) " \
                    "VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s); "
            
            val = (self.item_title, self.item_link, self.image_href, self.price, self.price_per_kg, self.clubcard_price, self.clubcard_price_per_kg)
            mycursor.execute(full_sql, val)
            mycursor.execute(temp_sql, val)
            mydb.commit()

            return
        
