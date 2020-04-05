#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2020/3/31 11:45
@Author  : cbz
@Site    : https://github.com/1173710224/brain-computing/blob/cbz
@File    : gui.py
@Software: PyCharm
@Descripe: 
"""
from experiment import aggregate_by_product
from experiment import rank_by_score
from experiment import fetch
from experiment import add_a_review


from tkinter import *
from tkinter import ttk
# global tmpshow
def aggregate():
    global tmpshow
    if tmpshow != None:
        tmpshow.destroy()
    ans = aggregate_by_product()
    tree = ttk.Treeview(top, show='headings');tree.pack()
    tree.place(width=top.winfo_width(), height=top.winfo_height(),x=0, y=0)
    # 定义列
    tree["columns"] = ("1", "2", "3")
    # 设置列属性，列不显示
    tree.column("1", width=100,anchor='center')
    tree.column("2", width=700)
    tree.column("3", width=100,anchor='center')

    # 设置表头
    tree.heading("1", text="product id")
    tree.heading("2", text="product title")
    tree.heading("3", text="number of reviews")

    index = 0
    for tmp in ans:
        tree.insert("",index,values=tmp)
    tmpshow = tree
    return
def rank():
    global tmpshow
    if tmpshow != None:
        tmpshow.destroy()
    ans = rank_by_score()
    tree = ttk.Treeview(top, show='headings');tree.pack()
    tree.place(width=top.winfo_width(), height=top.winfo_height(),x=0, y=0)
    # 定义列
    tree["columns"] = ("1", "2", "3","4")
    # 设置列属性，列不显示
    tree.column("1", width=100,anchor='center')
    tree.column("2", width=650)
    tree.column("3", width=100,anchor='center')
    tree.column("4", width=50,anchor='center')

    # 设置表头
    tree.heading("1", text="product id")
    tree.heading("2", text="product title")
    tree.heading("3", text="number of reviews")
    tree.heading("4", text="score")

    index = 0
    for tmp in ans:
        tree.insert("",index,values=tmp)
    tmpshow = tree
    return
def review():
    id = 0
    def get_data():
        id = int(entry.get())
        if id == 0 or id == None or id == "":
            print('bad id!')
            return
        ans = fetch(id)
        ans.reverse()
        tree = ttk.Treeview(frame, show='headings');tree.pack()
        tree.place(width=frame.winfo_width(), height=0.9 * frame.winfo_height(), x=0, y=0.2 * frame.winfo_height())
        # 定义列
        tree["columns"] = ("1", "2", "3", "4","5","6")
        # 设置列属性，列不显示
        tree.column("1", width=50, anchor='center')
        tree.column("2", width=100)
        tree.column("3", width=670)
        tree.column("4", width=80, anchor='center')
        tree.column("5", width=50, anchor='center')
        tree.column("6", width=50, anchor='center')
        # 设置表头star_rating, review_headline，review_body,review_date,vine,verified_purchased
        tree.heading("1", text="star")
        tree.heading("2", text="review headline")
        tree.heading("3", text="review body")
        tree.heading("4", text="review date")
        tree.heading("5", text="verified purchase")
        tree.heading("6", text="vine")

        index = 0
        for tmp in ans:
            # print(vine,purchase)
            if vine.get() == 1 and (tmp[5] == 'n' or tmp[5] == 'N'):
                continue
            if purchase.get() == 1 and (tmp[4] == 'n' or tmp[4] == 'N'):
                continue
            tree.insert("", index, values=(tmp[0],tmp[1],tmp[2],tmp[3],tmp[4],tmp[5]))
    global tmpshow
    if tmpshow != None:
        tmpshow.destroy()
    frame = Frame(top)
    frame.place(width=top.winfo_width(),height=top.winfo_height(),x=0,y=0)
    frame.update()
    entry = Entry(frame);entry.pack()
    entry.place(x=0.28*frame.winfo_width(),y=0.01*frame.winfo_height())

    vine = IntVar()
    b = Checkbutton(frame, variable=vine, text='is vine');b.pack()
    b.place(x=0.48*frame.winfo_width(),y=0.01*frame.winfo_height())

    purchase = IntVar()
    b = Checkbutton(frame, variable=purchase, text='verified purchase');b.pack()
    b.place(x=0.58*frame.winfo_width(),y=0.01*frame.winfo_height())

    b = Button(frame,text='search',command=get_data);b.pack()
    b.place(x=0.73*frame.winfo_width(),y=0.01*frame.winfo_height())
    tmpshow = frame
    return
def filter():
    return
def add():
    id = 0
    global tmpshow
    if tmpshow != None:
        tmpshow.destroy()
    def insert():
        input = [product.get(),customer.get(),purchase.get(),date.get(),str(head.get()),str(body.get()),star.get()]
        # input = [1,1,'n','8/31/2015','1','1',1]
        add_a_review(input)
        return
    frame = Frame(top)
    frame.place(width=top.winfo_width(),height=top.winfo_height(),x=0,y=0)
    frame.update()
    #product_id,customer_id,verified_purchase,review_date,review_headline,review_body,star_rating,
    product = Entry(frame);product.pack();l = Label(frame,text='#请输入评价的产品的id');l.pack();l.place(x=0.43*frame.winfo_width(),y=0.1*frame.winfo_height())
    product.place(x=0.28*frame.winfo_width(),y=0.1*frame.winfo_height())

    customer = Entry(frame);customer.pack();l = Label(frame,text='#请输入你的用户id');l.pack();l.place(x=0.43*frame.winfo_width(),y=0.2*frame.winfo_height())
    customer.place(x=0.28*frame.winfo_width(),y=0.2*frame.winfo_height())

    purchase = Entry(frame);purchase.pack();l = Label(frame,text='#输入n或者y表示你是否购买了该产品');l.pack();l.place(x=0.43*frame.winfo_width(),y=0.3*frame.winfo_height())
    purchase.place(x=0.28*frame.winfo_width(),y=0.3*frame.winfo_height())

    date = Entry(frame);date.pack();l = Label(frame,text='#输入评价的日期，格式如 8/31/2015');l.pack();l.place(x=0.43*frame.winfo_width(),y=0.4*frame.winfo_height())
    date.place(x=0.28*frame.winfo_width(),y=0.4*frame.winfo_height())

    head = Entry(frame);head.pack();l = Label(frame,text='#输入评论的标题');l.pack();l.place(x=0.43*frame.winfo_width(),y=0.5*frame.winfo_height())
    head.place(x=0.28*frame.winfo_width(),y=0.5*frame.winfo_height())

    body = Entry(frame);body.pack();l = Label(frame,text='#输入评论的内容');l.pack();l.place(x=0.43*frame.winfo_width(),y=0.6*frame.winfo_height())
    body.place(x=0.28*frame.winfo_width(),y=0.6*frame.winfo_height())

    star = Entry(frame);star.pack();l = Label(frame,text='#输入你对产品的打分，1到5的整数');l.pack();l.place(x=0.43*frame.winfo_width(),y=0.7*frame.winfo_height())
    star.place(x=0.28*frame.winfo_width(),y=0.7*frame.winfo_height())


    b = Button(frame,text='add',command=insert);b.pack()
    b.place(x=0.28*frame.winfo_width(),y=0.8*frame.winfo_height())
    tmpshow = frame
    return

top = Tk()
top.title('review dbms')
top.geometry('1000x600')
top.update()
global tmpshow
tmpshow = Label(top, text='welcome to pacifier review database management system', bg='green', font=('Times', 12), width=50, height=2);tmpshow.pack()
# b = Button(top,command=lambda :print(1));b.pack()

menu = Menu(top)
menu.add_command(label='aggregate',command=aggregate)
menu.add_command(label='ranking',command=rank)
menu.add_command(label='reviews',command=review)
menu.add_command(label='filter',command=review)
menu.add_command(label='add',command=add)
top['menu'] = menu

# 进入消息循环
top.mainloop()