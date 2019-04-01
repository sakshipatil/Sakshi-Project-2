from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
from flask import Flask,request, render_template, jsonify
from flask_cors import CORS
import time
from werkzeug import secure_filename
import imghdr
import os
import socket
import json
from bson import json_util

client = MongoClient('mongodb://localhost:27017/')
mydb = client.userDB
user = mydb.user


app = Flask(__name__)
api = Api(app)
CORS(app)

#To get IP Address
hostname = socket.gethostname()
IP = socket.gethostbyname(hostname)
ip_addr="http://"+str(IP)+":5000/"


# route for home page
@app.route('/')
def home():
    return render_template("teacher-list.html",ip_addr=ip_addr)
@app.route('/register')
def register():
    return render_template("register-teacher.html",ip_addr=ip_addr)

@app.route('/edit_user_id/<user_id>', methods=['POST','GET'])
def edit_teacher_id(user_id):
    iid = user_id
    c = user.find_one({"_id": int(iid)})
    return render_template("edit-teacher.html", data=c,ip_addr=ip_addr)

@app.route('/register_submit', methods=['POST','GET'])
def register_submit():
    try:
        c = user.find_one(sort=[("_id", -1)])["_id"]
        c = c + 1
    except:
        c = 1

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    address = request.form["address"]
    description = request.form["description"]

    mydict = {'_id': c,'first_name': first_name,'last_name':last_name,'email':email,'address':address,'description':description,'image':filenames}
    y = user.insert_one(mydict)
    return render_template("teacher-list.html")

@app.route('/edit_submit', methods=['POST','GET'])
def edit_submit():

    c = request.form["uid"]
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    address = request.form["address"]
    description = request.form["description"]

    mydict = {'first_name': first_name,'last_name':last_name,'email':email,'address':address,'description':description,'image':filenames}

    y = user.update_one({"_id" : int(c)},{"$set":mydict},upsert=False)
    return render_template("user_list.html")

@app.route('/all_users', methods=['GET'])
def all_users():
    cursor = user.find()
    l = []
    for document in cursor:
        l.append(document)
    data = {"teachers":l}
    ff = json.loads(json_util.dumps(data))
    return jsonify(ff)


if __name__ == '__main__':
    #app.run(debug=True)
    print("IP Address :",ip_addr)
    app.run(debug=True,host= '0.0.0.0')
