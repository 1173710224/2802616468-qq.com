import sqlite3
def test():
    conn = sqlite3.connect('review')
    # conn.execute('''CREATE TABLE COMPANY
    #        (ID INT PRIMARY KEY     NOT NULL,
    #        NAME           TEXT    NOT NULL,
    #        AGE            INT     NOT NULL,
    #        ADDRESS        CHAR(50),
    #        SALARY         REAL);''')
    c = conn.cursor()
    # c.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
    #       VALUES (1, 'Paul', 32, 'California', 20000.00 )")
    ans = c.execute('select * from company;')
    print(ans)
    for tmp in ans:
        print(tmp)
    conn.commit()
    conn.close()

'''
创建表结构
'''
def create_table(command):
    conn = sqlite3.connect('review')
    c = conn.cursor()
    c.execute(command)
    conn.commit()
    conn.close()
table_of_customer = '''CREATE TABLE CUSTOMER
       (id INT PRIMARY KEY     NOT NULL,
        vine    char(1)    NOT NULL);'''
table_of_product = '''CREATE TABLE PRODUCT
       (id INT PRIMARY KEY     NOT NULL,
        title text     ,
        category text  ,
        market_place      char(10));'''
table_of_review = '''CREATE TABLE REVIEW
       (id INT PRIMARY KEY     NOT NULL,
       product_id INT     NOT NULL,
       customer_id INT     NOT NULL,
       verified_purchase char(1) ,
       review_date char(10) NOT NULL,
       review_headline text NOT NULL,
       review_body text NOT NULL,
       star_rating int NOT NULL,
       total_votes int NOT NULL,
       helpful_votes int NOT NULL);'''


# create_table(table_of_customer)
# create_table(table_of_product)
# create_table(table_of_review)
'''
添加数据
'''
def insert(command):
    conn = sqlite3.connect('review')
    c = conn.cursor()
    c.execute(command)
    conn.commit()
    conn.close()
    return
def insert_customer(data):
    for tmp in data:
        x = str(tmp[0])
        y = 'n' if tmp[1] == 'n' or tmp[1] == 'N' else 'y'
        command = 'insert into customer (id,vine)\
        values(' + x + ',\'' + y + '\');'
        try:
            insert(command)
        except:
            continue
    return
def insert_product(data):
    for tmp in data:
        id = str(tmp[0])
        title = tmp[1].replace('"','')
        category = tmp[2].replace('"','')
        place = tmp[3]
        command = 'insert into product (id,title,category,market_place)\
        values(' + id + ',\"' + title + '\",\"' + category + '\",\'' + place + '\');'
        print(command)
        try:
            insert(command)
        except:
            continue
    return
def insert_review(data):
    id = 0
    for tmp in data:
        try:
            id += 1
            tmps = ''
            for i in range(len(tmp) - 1):
                if tmp[i] == str(tmp[i]):
                    tmp[i] = '\"' + tmp[i].replace('"', '') + '\"'
                tmps += str(tmp[i]) + ','
            tmps += str(tmp[len(tmp) - 1])
            command = 'insert into review (id,product_id,customer_id,verified_purchase,review_date,review_headline,review_body,star_rating,total_votes,helpful_votes)\
            values(' + str(id) + ',' + tmps + ')'
            insert(command)
        except:
            print(command)
            continue
    return
# import pandas as pd
# df = pd.read_csv('pacifier.csv')
# customers = df[['customer_id','vine']].values
# insert_customer(customers)
# products = df[['product_parent','product_title','product_category','marketplace']].values
# insert_product(products)
# reviews = df[['product_parent','customer_id','verified_purchase','review_date','review_headline','review_body',
#               'star_rating','total_votes','helpful_votes']].values
# insert_review(reviews)
# print('over!')
'''
实现功能
'''
def query():
    conn = sqlite3.connect('review')
    c= conn.cursor()
    command = 'SELECT id,vine from customer'
    ans = c.execute(command)
    print(ans.description)
    for tmp in ans:
        print(tmp)
        print(1)
        break
    conn.close()
    return
# query()
'''
按照product_id将每一条数据进行聚合，并且给出每个产品的评论条数
'''
def aggregate_by_product():
    # ids = query('select id from product')
    conn = sqlite3.connect('review')
    c= conn.cursor()
    ans = c.execute('select id,title from product')
    id2title = {}
    ids = []
    for id in ans:
        ids.append(id[0])
        id2title[id[0]] = id[1]
    dic = {}
    for id in ids:
        dic[id] = 0
    ans = c.execute('select product_id from review')
    for id in ans:
        dic[id[0]] += 1
    conn.close()
    ret = []
    ans = sorted(dic.items(), key=lambda x: x[1], reverse=False)
    for tmp in ans:
        ret.append((tmp[0],id2title[tmp[0]],tmp[1]))
    return ret

'''
将某个商品的所有的评分的平均分作为商品的评分，并按照这个分数进行排序，将1中的数据重新输出
'''
def rank_by_score():
    # ids = query('select id from product')
    conn = sqlite3.connect('review')
    c= conn.cursor()
    ans = c.execute('select id,title from product')
    id2title = {}
    ids = []
    for id in ans:
        ids.append(id[0])
        id2title[id[0]] = id[1]
    dic = {}
    total = {}
    for id in ids:
        dic[id] = 0
        total[id] = 0
    ans = c.execute('select product_id,star_rating from review')
    for id in ans:
        dic[id[0]] += 1
        total[id[0]] += id[1]
    for key in total.keys():
        total[key] = total[key] / dic[key]
    conn.close()
    ret = []
    ans = sorted(total.items(), key=lambda x: x[1], reverse=False)
    for tmp in ans:
        ret.append((tmp[0],id2title[tmp[0]],dic[tmp[0]],round(tmp[1],2)))
    return ret

'''
将某个商品的所有评论输出（按照日期排序），相应的信息只包括star_rating, review_headline，review_body,review_date,vine,verified_purchase
'''
def fetch(id):
    # ids = query('select id from product')
    conn = sqlite3.connect('review')
    c = conn.cursor()
    id2vine = {}
    ans = c.execute('select id,vine from customer')
    for tmp in ans:
        id2vine[tmp[0]] = tmp[1]
    ans = c.execute('select customer_id,star_rating,review_headline,review_body,review_date,verified_purchase from review where product_id='+str(id))
    ret = []
    for tmp in ans:
        tmpans = []
        for i in range(1,6):
            tmpans.append(tmp[i])
        tmpans.append(id2vine[tmp[0]])
        ret.append(tmpans)
    conn.close()
    return ret
'''
将3的结果按照vine和verified purchased进行筛选
'''
# 见GUI
'''
添加一条评论
'''
def insert_single_review(data):
    tmp = data
    tmps = ''
    for i in range(len(tmp) - 1):
        if tmp[i] == str(tmp[i]):
            tmp[i] = '\"' + tmp[i].replace('"', '') + '\"'
        tmps += str(tmp[i]) + ','
    tmps += str(tmp[len(tmp) - 1])
    command = 'insert into review (id,product_id,customer_id,verified_purchase,review_date,review_headline,review_body,star_rating,total_votes,helpful_votes)\
    values(' + tmps + ')'
    print(command)
    insert(command)
    return
def add_a_review(values):
    ids = set()
    customers = set()
    products = set()
    conn = sqlite3.connect('review')
    c= conn.cursor()
    command = 'select id from review'
    ans = c.execute(command)
    for tmp in ans:
        ids.add(tmp[0])
    ans = c.execute('select id from customer')
    for tmp in ans:
        customers.add(tmp[0])
    ans = c.execute('select id from product')
    for tmp in ans:
        products.add(tmp[0])
    conn.close()
    if not products.__contains__(values[0]):
        print('bad product id!')
        return
    if not customers.__contains__(values[1]):
        print('bad customer id!')
        return
    import random
    id = random.randint(100000000000000,999999999999999)
    while ids.__contains__(id):
        id = random.randint()
    values = [id] + values + [0,0]
    insert_single_review(values)
    print('add over!')
    return