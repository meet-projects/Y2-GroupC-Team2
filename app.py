from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
from flask_mail imprt Mail, Message
mail=Mail(app)
app.config['MAIL_SERVER']= 'smtp.gmail.com'
app.config['MAIL_PORT']= 465
app.config['MAIL_USERNAME']= 'poad7498@gmail.com'
app.config['MAIL_PASSWORD']= 'doaayoav'
app.config['MAIL_USE_SSL']= True
mail=Mail(app)


const firebaseConfig = {

  apiKey: "AIzaSyDVj6QQxX6ZotMxluwEMC58eST9HShAIUE",

  authDomain: "final2-e2f3e.firebaseapp.com",

  databaseURL: "https://final2-e2f3e-default-rtdb.europe-west1.firebasedatabase.app",

  projectId: "final2-e2f3e",

  storageBucket: "final2-e2f3e.appspot.com",

  messagingSenderId: "894344417219",

  appId: "1:894344417219:web:49d852ac015d452f717776"

databaseURL:"https://final2-e2f3e-default-rtdb.europe-west1.firebasedatabase.app/"
};

firebase=pyrebase.initialize_app(config)
db=firebase.database()
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

arabictext=[]
hebrewtext=[]
englishtext=[]
@app.route('/' , methods= ('POST', "get"))
def about():
    if request.method="POST":
        name=request.form['name']
        email=request.form['email']
        location= request.form['location']
        question=request.form['question']
        question={'name':name, 'email':email, 'location':locatoin, 'question':question}
        db.child('questoins').push(question)
@app.route('/admin')
def login_session():

#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)