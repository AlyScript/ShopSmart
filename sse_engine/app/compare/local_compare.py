import mysql.connector
import compare.operator as operator
import time
import re

def get_all_rows():
    result = list()
    mydb = mysql.connector.connect(
            host='dbhost.cs.man.ac.uk',
            user="h34567pv",
            password="Kekes-Database_Army+707++",
            database="2023_comp10120_z8"
        )
    cursor = mydb.cursor()
    
    sql = "SELECT * FROM AldiItems_TEMP;"
    cursor.execute(sql)
    aldi_result = cursor.fetchall()
    for row in aldi_result:
        result.append(list(row))
    
    sql = "SELECT * FROM SainsburysItems_TEMP;"
    cursor.execute(sql)
    for _row in cursor.fetchall():
            row = list(_row)
            row[0] = row[0] /10000 # Differentiate Aldi and Sainsburys IDs
            result.append(row)
    
    mydb.close()
    
    result = row_cleaner(result)
    return result

def row_cleaner(rows):
    # Remove weight references in titles.
    cleaned_rows = list()
    for row in rows:
        title = row[2]
        
        # Weight references
        title = re.sub(r'\b\w*\d+g\b', '', title)
        title = re.sub(r'\b\w*\d+kg\b', '', title)
        title = re.sub(r'\b\w*\d+cl\b', '', title)
        title = re.sub(r'\b\w*\d+ml\b', '', title)
        title = re.sub(r'\b\w*\d+l\b', '', title)
        
        # Brands
        title = title.replace('Specially Selected', '')
        
        row[2] = title
        cleaned_rows.append(row)
    
    return cleaned_rows

def gather_unmarked_titles(exclude, marked_ids, rows):
    title_id_pack = list()
    for row in rows:
        if row[0] in marked_ids or row[0] == exclude:
            continue
        else:
            title_id_pack.append([row[0], row[2]])
    return title_id_pack

def create_groups_table():
    mydb = mysql.connector.connect(
        host='dbhost.cs.man.ac.uk',
        user="h34567pv",
        password="Kekes-Database_Army+707++",
        database="2023_comp10120_z8"
    )
    
def commit_to_sql(group):
    mydb = mysql.connector.connect(
        host='dbhost.cs.man.ac.uk',
        user="h34567pv",
        password="Kekes-Database_Army+707++",
        database="2023_comp10120_z8"
    )
    
    base_id = group.pop(0)
    for id in group:
        mycursor = mydb.cursor()
        
        full_sql = "INSERT INTO ComparisonIDS " \
                   "(base_id, link_id) " \
                   "VALUES (%s, %s); "
                   
        ## NOTE: If the ID is less than 0, it is from Sainsburys. If it is greater than 0, it is from Aldi.
        
        val = (base_id, id)
        mycursor.execute(full_sql, val)
        mydb.commit()
    
    mydb.close()
    return

def run_local_compare():
    rows = get_all_rows()
    group_id_avail = 0
    marked_ids = list()
    groups = dict()
        
    for row in rows:
        id = row[0]
        title = row[2]
        new_group = list()
        
        if id in marked_ids:
            continue
        
        marked_ids.append(id)
        new_group.append(id)
        
        unmarked_title_pack = gather_unmarked_titles(exclude=id, marked_ids=marked_ids, rows=rows)
        titles = list()
        titles.append(title)
        titles.extend([title_pack[1] for title_pack in unmarked_title_pack])
        
        print("\n")
        print(f"🟥 BASE CASE {title} ID {id} NEWLEN {len(unmarked_title_pack)} / {len(rows)}")
        
        start = time.time()
        results = operator.operate_titles_threaded(titles, threads=1)
        results = results[1:] # Exclude the first title as it is the base case.
        end = time.time()
        delta = end-start
        
        print(delta)
        
        for result in results:
            index, match_title, is_similar, value = result
            if is_similar:
                print(f"🟪 MATCH FOUND -- {title} to {match_title} || {id} -> {unmarked_title_pack[index][0]} || {round((value*100), 3)}%")
                marked_ids.append(unmarked_title_pack[index][0])
                new_group.append(unmarked_title_pack[index][0])
        
        if len(new_group) > 1:
            print(f"Forming new group LEN {len(new_group)}")
            groups[group_id_avail] = new_group
            group_id_avail += 1
            commit_to_sql(new_group)
    
    print(f"{len(groups)} Groups Formed")

run_local_compare()        