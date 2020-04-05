#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2020/3/31 2:46
@Author  : cbz
@Site    : https://github.com/1173710224/brain-computing/blob/cbz
@File    : test.py
@Software: PyCharm
@Descripe: 
"""
import sqlite3

conn = sqlite3.connect('review')
c = conn.cursor()
command = 'select * from review where customer_id = 1'
# command = 'delete from review where customer_id = 1'
ans = c.execute(command)
for tmp in ans:
    print(tmp)
# conn.commit()
conn.close()

# from experiment import aggregate_by_product
# from experiment import aggregate_by_product
# ans = aggregate_by_product()