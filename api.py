from flask import*
import pymongo
from defa import responsee
from bson import ObjectId
import string
import random
app = Flask(__name__)
myclient = pymongo.MongoClient("")
mydb = myclient["heritage"]
myadmin = mydb["admin"]
myusers = mydb["users"]
mytok = mydb["tokenn"]

def random_generate(lenght):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(lenght))

new_token=random_generate(30)

@app.route("/admin",methods=["POST","GET"])
def admin():
    try:
        x = myadmin.find_one({"user":request.json["user"],"password":request.json["password"]})
        if x:
            error_response = responsee.response.successres("Login successfully")
            return error_response.__dict__
        else:
            error_response = responsee.response.Errorres(400, "User Or Password Wrong!!")
        return error_response.__dict__
    except Exception as e:
        error_response = responsee.response.Errorres(400, str(e))
        return error_response.__dict__

@app.route("/admin/user",methods=["POST","GET"])
def user():
    try:
        hh = request.json["user"] 
        x = request.json["password"]
        
        res = myusers.find_one({"user":hh})
        if res:
            error_response = responsee.response.Errorres(400, "This User already Used!!")
            return error_response.__dict__
        else:
            d = {"user":hh,
                "password":x,
                "status":True}
            myusers.insert_one(d)
            error_response = responsee.response.successres("User Created")
            return error_response.__dict__

    except Exception as e:
        error_response = responsee.response.Errorres(400, str(e))
        return error_response.__dict__

@app.route("/getuser",methods=["GET"])
def get():
    try:
        x=myusers.find({})
        xx=[]
        for z in x:
            z ["_id"]=str(z["_id"])
            xx.append(str(z))
        return json.dumps(xx)
    except Exception as e:
        error_response = responsee.response.Errorres(400, str(e))
        return error_response.__dict__

        

@app.route("/update")
def update():
    try:
        mycolz = mydb["users"]
        z=request.json["_id"]
        x=request.json["status"]
        xz = mycolz.find_one({"_id" : ObjectId(z)})
        if xz:
            myquery = { "_id": ObjectId(z) }
            newvalues = { "$set": { "status": x } }
            myusers.update_one(myquery, newvalues)
            error_response = responsee.response.successres("Done")
            return error_response.__dict__

        else:
            error_response = responsee.response.Errorres(400, "Cannot find this user")
            return error_response.__dict__
    except Exception as e:
        error_response = responsee.response.Errorres(400,"Cannot update something wrong")
        return error_response.__dict__

@app.route("/userlogin" , methods=["GOT","POST"])
def user_login():
    try:
        us = request.json["user"]
        pas = request.json["password"]
        zx = myusers.find_one({"user":us,"password":pas})
        if zx:
            
            if zx["status"]:
                d={"_id":zx["_id"],
                "token":new_token}
                inn=mytok.insert_one(d)
                ff={"status_code:":200,
                    "msg":"Login successfully",
                    "you token = ":new_token}
                return ff
            else:
                error_response = responsee.response.Errorres(400,"User not active")
                return error_response.__dict__

        else:
            error_response = responsee.response.Errorres(400,"User Or Pass Wrong!!")
            return error_response.__dict__
    except Exception as e:
        error_response = responsee.response.Errorres(400,str(e))
        return error_response.__dict__

app.run(debug=True)