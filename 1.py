from flask import Flask,render_template,request
# from flask_mysqldb import MySQL
app=Flask(__name__)
import pymongo
# app.secret_key = "testing"
client = pymongo.MongoClient("mongodb+srv://jayadeep:jayadeep@cluster0.jd9mv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.get_database('total_records')
register = db.register

"""
funtion: home:: does not take any parameters

returns:: This function returns render template in html format
"""

@app.route('/')
def home():
    
    return render_template("signup.html")


"""
funtion: signup:: It will check all email validations for register user and 
                    does not take any parameters

returns:: This function returns render template in html format
"""

@app.route('/mynext',methods=["GET","POST"])
def signup():
    username=request.form.get("username")
    password=request.form.get("password")
    phonenumber=request.form.get("phonenumber")
    email=request.form.get("email")

    
    
    if (verify_Email(email) and  verify_password(password) and verify_phonenumber(phonenumber)):
        register.insert_one({"email":email,"phone_no":phonenumber,"user_name":username,"password":password})
        # print(username,password,phonenumber,email)
        return render_template("login.html")
    else:
        return render_template("error.html")


"""
funtion: verify_Email:: This wil check the email format is valid or not 
                        and does not take any parameters

returns:: This function returns true or false
"""
def verify_Email(email):
    if(email.find("@")!=-1 and email.find(".")!=-1):
        print("valid email")
        return True
    else:
        print("not valid email")
        return False


"""
funtion: verify_password:: This wil check the password format  is valid or not and check the required validations
                        and does not take any parameters

returns:: This function returns true or false
"""
def verify_password(password):
          
    SpecialSym =['$', '@', '#', '%']
    val = True
      
    if len(password) < 8:
        print('length should be at least 8')
        val = False
    
    if not any(char.isdigit() for char in password):
        print('Password should have at least one numeral')
        val = False
    if not any(char.isupper() for char in password):
        print('Password should have at least one uppercase letter')
        val = False
          
    if not any(char.islower() for char in password):
        print('Password should have at least one lowercase letter')
        val = False
          
    if not any(char in SpecialSym for char in password):
        print('Password should have at least one of the symbols $@#')
        val = False
    if val:
        return val



"""
funtion: verify_phonenumber:: This wil check the phonenumber format  is valid or not and check the required number validations
                        and does not take any parameters

returns:: This function returns number valid or not
"""

import re
def verify_phonenumber(phonenumber):
    phonenumber=str(phonenumber)
    if(len(phonenumber))==10 and (phonenumber.isdigit()):
        output = re.findall(r"^[6789]\d{9}$",phonenumber)
        if(len(output)==1
        ):
            print("valid phonenumber")
            return True
        else:
            print("Invalid phone number")
            return False
    else:
        print("Invalid")
        return False


"""
funtion: login:: This will check the register email is matching with entered email or not.

returns:: This will return the render template post format
"""

@app.route('/prev',methods=["GET","POST"])
def login():
    email=request.form.get("email")
    password=request.form.get("password")
    exits=register.find_one({"email":email,"password":password})
    print(exits)
    if(exits):

        return render_template("dashboard.html")
    else:
        return render_template("error.html")


    #     print("invalid")


"""
funtion: verify:: This will send the msg that entered emaiul is verified.

returns:: This will return the render template post format
"""
@app.route('/verify',methods=["GET","POST"])
def verify():
    return render_template("verification.html")






if __name__=='main_':
    app.run(debug=True)



    