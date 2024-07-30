import mysql.connector

def generate_dod(count=20):
    mydb = mysql.connector.connect(
            host='dbhost.cs.man.ac.uk',
            user="h34567pv",
            password="Kekes-Database_Army+707++",
            database="2023_comp10120_z8"
        )
    cursor = mydb.cursor()
    
    sql = "SELECT * FROM ComparisonIDS;"
    cursor.execute(sql)
    comparisons = cursor.fetchall()
    filtered = []
    ## Filtered --> ALDI, SAINS ID.

    for _block in comparisons:
        block = []
        if (_block[1] < 1 and _block[2] > 1):
            block = [_block[2], (_block[1] * 10000)]
        elif (_block[1] > 1 and _block[2] < 1):
            block = [_block[1], round((_block[2] * 10000), 0)]
        else:
            continue
        
        processed_block = [block[0], block[1]]
            
        sql = 'SELECT price_per_kg FROM AldiItems_TEMP WHERE id = ' + str(block[0]) + ';'
        cursor.execute(sql)
        aldi_price = cursor.fetchall()[0][0]
        
        sql = 'SELECT nectar_price_per_kg FROM SainsburysItems_TEMP WHERE id = ' + str(block[1]) + ';'
        cursor.execute(sql)
        sainsburys_price = cursor.fetchall()[0][0]
        
        if sainsburys_price == 0.0:
            sql = 'SELECT price_per_kg FROM SainsburysItems_TEMP WHERE id = ' + str(block[1]) + ';'
            cursor.execute(sql)
            sainsburys_price = cursor.fetchall()[0][0]
        
        delta = abs(aldi_price - sainsburys_price)
        processed_block.append(delta)
        
        filtered.append(processed_block)
    
    mydb.close()
    ## Order Them by best to worst.
    filtered.sort(key=lambda x: x[2])
    filtered = filtered[(-1*count):]
    filtered.reverse()
    return filtered

def commit_dod(dod_list):
    mydb = mysql.connector.connect(
        host='dbhost.cs.man.ac.uk',
        user="h34567pv",
        password="Kekes-Database_Army+707++",
        database="2023_comp10120_z8"
    )
    
    mycursor = mydb.cursor()
    sql = 'DELETE FROM DOD_List;'
    mycursor.execute(sql)
    mydb.commit()
    
    for dod in dod_list:
        mycursor = mydb.cursor()
        
        full_sql = "INSERT INTO DOD_List " \
                   "(aldi_id, sainsburys_id, delta) " \
                   "VALUES (%s, %s, %s); "
        
        val = (dod[0], dod[1], dod[2])
        mycursor.execute(full_sql, val)
        mydb.commit()
    
    mydb.close()
    return

def run_dod_gen(count=20):
    dod_list = generate_dod(count=count)
    print(len(dod_list))
    commit_dod(dod_list)
    return

run_dod_gen(20)