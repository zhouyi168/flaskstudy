#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:末夏
@file: register.py
@time: 2021/06/02
"""

from flask import Flask,jsonify,request,render_template

import json
import re
from common import constant
from common.database import DataBase
import time

app=Flask(__name__,template_folder='templates')
app.config['JSON_AS_ASCII']=False



@app.route("/")
@app.route("/register")
def get_register_page():
    return render_template('register.html')

def get_telephones():
    db = DataBase()
    sql="SELECT DISTINCT telephone FROM user ORDER BY telephone"
    tel=[]
    for i in db.fetchall(sql):
        tel.append(i[0])
    return tel
def get_username():
    db = DataBase()
    sql = "SELECT DISTINCT username FROM user ORDER BY username"
    users = []
    for i in db.fetchall(sql):
        users.append(i[0])
    return users
def get_password(username):
    db = DataBase()
    sql = 'SELECT password FROM user where username="{}"'.format(username)
    password=[]
    for i in db.fetchall(sql):
        password.append(i[0])
    return password


@app.route("/registerserver",methods=["POST"])
def registerserver():
    try:
        # data = json.loads(request.get_data())
        # print(data)
        # username=data['username']
        # password=data['password']
        # sex=data['sex']
        # telephone=data['telephone']
        # address=data['address']
        username = request.form['username'].strip()
        password=request.form['password'].strip()
        sex=request.form['sex'].strip()
        telephone=request.form['telephone'].strip()
        address=request.form['address'].strip()
        if username and password and telephone:
            if username in get_username():
                msg = {"code": 20001, "msg": "用户名已经存在，不能重复注册"}
                return render_template("error.html", **msg)
            elif sex not  in ("男","女"):
                msg={"code":20002,"msg":"性别参数错误"}
                return render_template("error.html", **msg)
            elif len(telephone)!=11 or re.match("^1[3578]\d{9}$",telephone) is None:
                msg={"code":20003,"msg":"手机格式错误"}
                return render_template("error.html", **msg)
            elif telephone in get_telephones():
                msg={"code":20005,"msg":"手机已经存在，不能重复注册"}
                return render_template("error.html", **msg)
            else:
                db = DataBase()
                p=(username,password,sex,telephone,address)
                sql="INSERT INTO user(username,password,sex,telephone,address) VALUES(?,?,?,?,?) "
                db.insert(sql=sql,p=p)
                return render_template('success.html')
        else:
            msg={"code":20004,"msg":"用户名或者密码或者电话号码不能为空"}
            return render_template("error.html", **msg)
    except Exception as e:
        error=request.headers
        msg='出错了，请联系开发人员:{}'.format(error)
        return render_template("error.html", msg=msg)

# @app.route("/login",methods=["POST"])
# def add(a,b):
#     if type(a) is int and type(b) is int:
#         return str(a+b)
#     elif type(a) != int:
#         return "type error:a"
#     elif type(b) is not  int:
#         return "type error:b"
@app.route("/login")
def enterLoginPage():
    return render_template("login.html",userError="",pwdError="")
@app.route("/loginSubmit",methods=["POST"])
def loginSubmit():
    username=request.form["username"].strip()
    password=request.form["password"].strip()
    if username and password:
        if username not in get_username():
            return render_template("login.html",userError="用户名不存在",pwdError='')

        elif password not in get_password(username):
            return render_template("login.html",userError='',pwdError="密码错误")
        else:
            return render_template("loginSuccess.html")
    elif username=='':
        return render_template("login.html", userError="用户名不能为空", pwdError=password)
    elif password=='':
        return render_template("login.html", userError=username, pwdError="密码不能为空")
    elif username=='' and password=='':
        return render_template("login.html",userError="用户名不能为空",pwdError="密码不能为空")

def get_date():
    return time.strftime('%Y-%m-%d',time.localtime())

@app.route("/search")
def intoSearchPage():
    return render_template("info.html",u='',p='',begintime='1970-01-01',endtime=get_date())

def get_by_date(begint,endt):
    sql='SELECT id,title,pv,uploaddata,nowdata FROM info WHERE uploaddata BETWEEN "{}" AND "{}"'.format(begint,endt)
    db=DataBase()
    return db.fetchall(sql)

def get_by_title(title):
    sql='SELECT id,title,pv,uploaddata,nowdata FROM info WHERE title="{}"'.format(title)
    db=DataBase()
    return db.fetchall(sql)

def get_by_all(title,begint,endt):
    sql='SELECT id,title,pv,uploaddata,nowdata FROM info WHERE title="{}" and uploaddata BETWEEN "{}" AND "{}"'.format(title,begint,endt)
    db=DataBase()
    return db.fetchall(sql)
def get_all():
    sql='SELECT id,title,pv,uploaddata,nowdata FROM info'
    db=DataBase()
    return db.fetchall(sql)


@app.route("/doSearch", methods=["POST"])
def doSearch():
    title=request.form.get('title')
    begintime=request.form.get('begintime')
    endtime=request.form.get('endtime')
    if title and begintime and endtime:
        u=get_by_all(title,begintime,endtime)
        if u:
            return render_template("info.html",u=u,p='',begintime=begintime,endtime=endtime)
        else:
            return render_template("info.html", u='', p='无查询结果',begintime=begintime,endtime=endtime)
    elif title=='' and begintime=='' and endtime=='':
        u=get_all()
        return render_template("info.html",u=u,p='',begintime=begintime,endtime=endtime)
    elif title and begintime=='' and endtime=='':
        u=get_by_title(title)
        return render_template("info.html",u=u,p='',begintime=begintime,endtime=endtime)
    elif title=='' and begintime and endtime:
        u=get_by_date(begintime,endtime)
        return render_template("info.html", u=u, p='',begintime=begintime,endtime=endtime)
    else:
        return render_template("info.html", u='', p='无查询结果',begintime=begintime,endtime=endtime)



if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)