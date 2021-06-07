#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:末夏
@file: database.py
@time: 2021/04/13
"""

import sqlite3
from common import constant
class DataBase:
    def __init__(self):
        self.conn=sqlite3.connect(constant.db_url)

    def insert(self,sql,p):
        try:
            # c=self.conn.cursor()
            self.conn.execute(sql,p)
            self.conn.commit()
            print("Operation done successfully")
        except Exception as e:
            raise e

    def exec(self,sql):
        try:
            c=self.conn.cursor()
            c.execute(sql)
            c.close()
            self.conn.commit()
        except Exception as e:
            raise e

    def rowcount(self,sql):
        return (len(self.fetchall(sql)))

    def columncount(self,sql):
        return (len(self.fetchall(sql)[0]))


    def fetchall(self,sql):
        c=self.conn.cursor()
        c.execute(sql)
        res=c.fetchall()
        c.close()
        self.conn.commit()
        self.conn.close()
        return res

    def fetchone(self,sql):
        c = self.conn.cursor()
        c.execute(sql)
        res = c.fetchone()
        c.close()
        self.conn.commit()
        return res
    def __del__(self):
        self.conn.close()

def insert(sql,p):
    conn=sqlite3.connect(constant.db_url)
    print(constant.db_url)
    c=conn.cursor()
    c.execute(sql,p)
    conn.commit()
    conn.close()
if __name__=="__main__":
    db=DataBase()
    sql = "SELECT DISTINCT telephone FROM user ORDER BY telephone"
    T=db.fetchall(sql)
    tel=[]
    for i in T:
        tel.append(i[0])

    print(tel)

    # conn=DataBase()
    # title='大爱无疆1'
    # u='https\://v.qq.com/x/cover/mzc002001ixg5do.html'
    # pv='104.8万'
    # p=(title,u,pv)
    # insert(sql="INSERT INTO info(title,url,pv)VALUES(?,?,?)",p=p)




