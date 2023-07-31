from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
from flask_mail import Mail, Message
import random 


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
        if request.form [popular]==True:
            question_and_awnser=db.child('questions').child(UID).get().val()
            question_and_awnser['awnser']= request.form['awnser']
            db.child('popular').push(question_and_awnser )
        db.child('questions').child(login_session['UID']).remove()
        return render_template('admin.html')
    else:
        try:
            print (login_session['localId'])
        except:
            return redirect(url_for('awnser'))
    try:
        UID = random.choice(list(db.child('questions').get().val()))
        loggin_session['UID']= UID    
        value=db.child('questions').get().val()[UID]
        login_session['recipientemail']= value['email']
        return render_template('admin.html', question=value)
    except: 
        return "all questions awnsered"

@app.route("/signout")
def signout():
    auth.current_user=None
    login_session['user']=None
    return (redirect(url_for('about')))


@app.route('/home', methods=['POST','GET'])
@app.route('/home/<string:language>' ,methods=['POST', 'GET'])
def home(language='he'):
    language = language.lower()
    return render_template('home.html', text= db.child('langueges').child(language).get().val())

if __name__ == '__main__':
    app.run(debug=True)