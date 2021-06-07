#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:末夏
@file: constant.py
@time: 2021/06/04
"""
import os

base_url=os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
common_url=os.path.join(base_url,"common")
app_url=os.path.join(base_url,"app")
templates_url=os.path.join(base_url,"templates")
datas_url=os.path.join(base_url,"datas")
database_url=os.path.join(datas_url,'database')
db_url=os.path.join(database_url,'flaskstudy.db')