import tesco.locators as locators
import tesco.cat_handler as cat_handler
import mysql.connector

def wipe_temp_table():
    mydb = mysql.connector.connect(
        host='dbhost.cs.man.ac.uk',
        user="h34567pv",
        password="Kekes-Database_Army+707++",
        database="2023_comp10120_z8"
    )
    
    mycursor = mydb.cursor()
    sql = 'DELETE FROM TescoItems_TEMP;'
    mycursor.execute(sql)
    mydb.commit()
    mycursor.close()
    mydb.close()


def run_all():
    extension_list = locators.collate_extension_list()
    total_built_items = list()
    
    for index, extension in enumerate(extension_list):
        print(f"--- Building Page {index + 1} / {len(extension_list)} : {extension} ---")
        loc_items = cat_handler.build_category(extension)
        total_built_items.extend(loc_items)
    
    return total_built_items

print(len(run_all()))