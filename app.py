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
app.config['MAIL_USERNAME']= 'shekulutov@outlook.com'
app.config['MAIL_PASSWORD']= 'Adampolina'
app.config['MAIL_USE_SSL']= True
mail=Mail(app)

auth= firebase.auth()


arabictext=[]
hebrewtext=[]
db.child
@app.route('/' , methods= ('POST', "get"))
def about():
    if request.method=="POST":
        name=request.form['name']
        email=request.form['email']
        location= request.form['location']
        question=request.form['question']
        question={'name':name, 'email':email, 'location':location, 'question':question}
        db.child('questions').push(question)
    try:
        FAQ= db.child ('popular').get().val()
        FAQ=list(FAQ.values())
    except:
        FAQ=[]
    return render_template('about.html', FAQ=FAQ)
@app.route('/admin' , methods=['POST', 'GET'])
def adminlogin():
    if request.method=='POST':
        username= request.form['username']
        password = request.form['password']
        try:
            login_session['user']=auth.sign_in_with_email_and_password(username, password)
            return redirect(url_for('answer'))
        except Exception as e:
            return(f'{e}')
            return render_template('adminlogin.html')
    else:
        return render_template('adminlogin.html')
@app.route ('/Answers', methods=['POST', 'GET'])
def answer():
    if request.method=='POST':
        msg= Message('Answer for question about out charity "shekulutov"', sender="poad7498@gmail.com", recipients= login_session['recipientemail'] )
        msg.body= request.form['answer']
        mail.send(msg)
        if request.form [popular]==True:
            question_and_answer=db.child('questions').child(UID).get().val()
            question_and_answer['answer']= request.form['answer']
            db.child('popular').push(question_and_answer )
        db.child('questions').child(login_session['UID']).remove()
    else:
        try:
            print (login_session['user'])
        except:
            return redirect(url_for('adminlogin'))

    UID = random.choice(list(db.child('questions').get().val()))
    login_session['UID']= UID    
    value=db.child('questions').get().val()[UID]
    print (1000000000000000000)
    print (value)
    login_session['recipientemail']= value['email']
    return render_template('admin.html', question=value)
    # except: 
    #     return "all questions answered"

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