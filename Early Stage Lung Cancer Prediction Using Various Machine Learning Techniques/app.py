from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np


from flask import Flask,request, url_for, redirect, render_template
import pandas as pd
import numpy as np
import pickle
import sqlite3
import os



app = Flask(__name__)



model_name1 = open("model.pkl","rb")
model = pickle.load(model_name1)




@app.route('/')
def hello_world():
    return render_template("hello.html")

@app.route('/logon')
def logon():
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('signin.html')

@app.route("/signup")
def signup():

    username = request.args.get('user','')
    name = request.args.get('name','')
    email = request.args.get('email','')
    number = request.args.get('mobile','')
    password = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("insert into `info` (`user`,`email`, `password`,`mobile`,`name`) VALUES (?, ?, ?, ?, ?)",(username,email,password,number,name))
    con.commit()
    con.close()
    return render_template("signin.html")

@app.route("/signin")
def signin():

    mail1 = request.args.get('user','')
    password1 = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `user`, `password` from info where `user` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()

    if data == None:
        return render_template("signin.html")    

    elif mail1 == 'admin' and password1 == 'admin':
        return render_template("index.html")

    elif mail1 == str(data[0]) and password1 == str(data[1]):
        return render_template("index.html")
    else:
        return render_template("signup.html")



@app.route('/predict2',methods=['POST','GET'])
def predict2():
    text1 = request.form['1']
    text2 = request.form['2']
    text3 = request.form['3']
    text4 = request.form['4']
    text5 = request.form['5']
    text6 = request.form['6']
    text7 = request.form['7']
    text8 = request.form['8']
    text9 = request.form['9']
    text10 = request.form['10']
    text11 = request.form['11']
    row_df = np.array([text1,text2,text3,text4,text5,text6,text7,text8,text9,text10,text11])
    row_df  = row_df.reshape(1,-1)
    print(row_df)
    prediction=model.predict_proba(row_df)
    output='{0:.{1}f}'.format(prediction[0][1], 2)
    output = str(float(output)*100)+'%'
    print(output)
    if output>str(0.6):
        return render_template('index.html',pred=f'You have High chance of having Lung cancer.')
    elif output<str(0.4):
        return render_template('index.html',pred=f'You have Low chance of having Lung cancer.')
    else:
        return render_template('index.html',pred=f'You have Medium chance of having Lung cancer.')



@app.route('/index')
def index():
	return render_template('index.html')


@app.route('/home')
def home():
	return render_template('home.html')



if __name__ == '__main__':
    app.run(debug=True)
