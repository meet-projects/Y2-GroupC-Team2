from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
from flask_mail import Mail, Message
import random 
from googletrans import Translator
translator = Translator()
config = {

  'apiKey': "AIzaSyDVj6QQxX6ZotMxluwEMC58eST9HShAIUE",

  'authDomain': "final2-e2f3e.firebaseapp.com",

  'databaseURL': "https://final2-e2f3e-default-rtdb.europe-west1.firebasedatabase.app",

  'projectId': "final2-e2f3e",

  'storageBucket': "final2-e2f3e.appspot.com",

  'messagingSenderId': "894344417219",

  'appId': "1:894344417219:web:49d852ac015d452f717776",

'databaseURL':"https://final2-e2f3e-default-rtdb.europe-west1.firebasedatabase.app/"
};

firebase=pyrebase.initialize_app(config)
db=firebase.database()
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

mail=Mail(app)
app.config['MAIL_SERVER']= 'smtp.gmail.com'
app.config['MAIL_PORT']= 465
app.config['MAIL_USERNAME']= 'poad7498@gmail.com'
app.config['MAIL_PASSWORD']= 'doaayoav'
app.config['MAIL_USE_SSL']= True
mail=Mail(app)

auth= firebase.auth()


arabictext=[]
hebrewtext=[]
englishtext=[]
@app.route('/' , methods= ('POST', "get"))
def about():
    if request.method=="POST":
        name=request.form['name']
        email=request.form['email']
        location= request.form['location']
        question=request.form['question']
        question={'name':name, 'email':email, 'location':location, 'question':question}
        db.child('questions').push(question)
    return render_template('about.html')
@app.route('/admin')
def adminlogin():
    if request.method=='POST':
        username= request.form[ 'username']
        password = request.form ['password']
        if db.child('auth').get().val()[username]==password:
            login_session['user']=auth.sign_in_with_email_and_password(username, password)
            return redirect(url_for('admin'))
    else:
        return render_template('adminlogin.html')
@app.route ('/Answers', methods=['POST', 'GET'])
def awnser():
    if request.method=='POST':
        msg= Message('Awnser for question about out charity "shekulutov"', sender="poad7498@gmail.com", recipients= login_session['recipientemail'] )
        msg.body= request.form[awnser]
        mail.send(msg)
        return render_template('admin.html')
    else:
        try:
            print (login_session['localId'])
        except:
            return redirect(url_for('awnser'))
    UID = random.choice(list(db.child('questions').get().val()))
    value=db.child('questions').get().val()[UID]
    login_session['recipientemail']= value['email']
    db.child('questions').child(UID).remove()
    return render_template('admin.html', question=value)
content = "This is a paragraph about a product !"
@app.route('/test')
def test():
    translated = translator.translate(content,'ar')
    return render_template('test.html',tr = translated.text)

if __name__ == '__main__':
    app.run(debug=True)