import pymysql
from flask import Flask, request, redirect, render_template,jsonify
import re
from flask import Flask,render_template,request,jsonify
from chat import get_response 
#import mysql.connector


# Connect to the database
conn = pymysql.connect(host="localhost", user="root", password="root123", db="ab")

# Create the Flask app
app = Flask(__name__)

# Route for the login page
@app.route("/", methods=["GET", "POST"])
def logindemo():
    if request.method == "POST":
        # Get the user inputs
        username = request.form["username"]
        password = request.form["password"]
        account={}

        # Verify the inputs
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM accounts1 WHERE username=%s AND password=%s', (username,password,))
        account=cursor.fetchone()
        cursor.close()
        
        data=account[3]
        if data=='admin':
            return render_template("admin.html")
        else:
            return render_template("index.html", error="Invalid username or password.")
      
    return render_template("logindemo.html")
@app.route('/register', methods =['GET', 'POST'])
def register():
 msg = ''
 if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
  username = request.form['username']
  password = request.form['password']
  email = request.form['email']
  type ='user'
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM accounts1 WHERE username = % s', (username, ))
  account = cursor.fetchone()
  if account:
   msg = 'Account already exists !'
  elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
   msg = 'Invalid email address !'
  elif not re.match(r'[A-Za-z0-9]+', username):
   msg = 'Username must contain only characters and numbers !'
  elif not username or not password or not email:
   msg = 'Please fill out the form !'
  else:
    cursor.execute('INSERT INTO accounts1 VALUES ( % s, % s, % s,%s)', (username, password,email,type,))
    cursor.connection.commit()
    msg = 'You have successfully registered !'
    return render_template('logindemo.html')
 elif request.method == 'POST':
  msg = 'Please fill out the form !'
 return render_template('register.html')
@app.route("/home")
def home():
    return render_template("home.html")
@app.route("/menu")
def menu():
    return render_template('menu.html')
@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/help")
def help():
    return render_template('help.html')
@app.route("/love")
def love():
    return render_template('love.html')
@app.route("/gym")
def gym():
    return render_template('gym.html')
@app.route("/chillout")
def chillout():
    return render_template('chillout.html')
@app.route("/sad")
def sad():
    return render_template('sad.html')
# @app.route("/index_get")
# def index_get():
#     return render_template("base.html")

@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method=='POST':
        text=request.get_json().get("message")
        response =get_response(text)
        message ={"answer":response}
        return jsonify(message)
@app.route("/mbot")
def mbot():
    return render_template('mbot.html')
#@app.route('/logindetails',methods=['GET','POST'])
#def logindetails():
  #cursor = conn.cursor()
  #cursor.execute("SELECT * FROM accounts1")
  #data=cursor.fetchall()
  #print(type(data[0]))
  #cursor.close()
  #return render_template('logindetails.html',data=data)
@app.route('/logindetails', methods=['GET', 'POST'])
def logindetails():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accounts1")
    account_data = cursor.fetchall()
    cursor.close()
    return render_template('logindetails.html', account_data=account_data)
@app.route('/reviewk')
def reviewk():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM review")
    order_data = cursor.fetchall()
    cursor.close()
    return render_template('reviewk.html',  order_data= order_data)


@app.route('/reviews', methods =['POST'])
def reviews():
    name = request.form['name']
    email = request.form['email']
    message = request.form['msg']
    cursor = conn.cursor()
    cursor.execute('INSERT INTO review VALUES ( % s, % s, % s)', (name,email,message,))
    cursor.connection.commit()
    return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)