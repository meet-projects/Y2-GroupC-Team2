from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
from flask_mail import Mail, Message
import random 
import jinja2


config = {
  'apiKey': "AIzaSyDVj6QQxX6ZotMxluwEMC58eST9HShAIUE",
  'authDomain': "final2-e2f3e.firebaseapp.com",
  'databaseURL': "https://final2-e2f3e-default-rtdb.europe-west1.firebasedatabase.app",
  'projectId': "final2-e2f3e",
  'storageBucket': "final2-e2f3e.appspot.com",
  'messagingSenderId': "894344417219",
  'appId': "1:894344417219:web:49d852ac015d452f717776",
  'databaseURL':"https://final2-e2f3e-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase=pyrebase.initialize_app(config)
db=firebase.database()
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

mail=Mail(app)

app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'shekulutov@outlook.com'
app.config['MAIL_PASSWORD'] = 'Adampolina'
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USE_TLS'] = True

mail=Mail(app)

auth= firebase.auth()


# db.child('langueges').child('ar').set(['تقود مجموعة Shekulo Tov "شيكلو توف" وتطور أطر إعادة تأهيل فعالة ورائدة. تعمل المجموعة على تغيير حياة الأشخاص ذوي الإعاقة في إسرائيل وحول العالم','خدماتنا' ,'مهنة في المجموعة' ,'خدمات للشركات',' متلقي خدمات في المجموعات',' وحدات تدريب',' مهني',' الانخراط في سوق' ,' متلقو الخدمة الذين ','انخرطوا في سوق العمل' ,' المناسبات الاجتماعية','التي حدثت في المجموعات ',' المنظمات التي تعمل معنا لتوظيف الأشخاص  التي معها إعاقات','عامل في المجموعة','*مجموعة ','شيكلو توف' ,'لا تقبل التبرعات ولا توظف المتطوعين','عن المجموعة','خدمات للشركات ','التأهيل المهني','إعادة التأهيل الاجتماعي','خدمات تشغيلية اجتماعية ترفيهية','لمزيد من المعلومات','مهنة في المجموعة','هل تبحث عن عمل هادف ومركز ؟','انضم الينا' ,'لجميع الوظائف','مدير فرع دندشة في ريشون لتسيون','منطقة المركز -وظيفة% 100','منسق,ة التوظيف في العفولة عفولة 50%','عامل في المصنع في موشاف منطقة المركز -وظيفة 75%', 'حولنا','عن المجموعة','  النشاط الدولي', 'مهنة في المجموعة','كتب عنا','خدماتنا','المشاريع الجماعية','محتوياتنا', 'مدونة','VOD كل هذا جيد ','خدمات للشركات',  'توظيف الأشخاص ذوي الإعاقة' ,'خدمات ومنتجات الشركات', 'قم بإنشاء مفتاح','عربي/ عبراني' ,'مهنة' ,'شيكلوتوف','توظيف الأشخاص',' ذوي الإعاقة','التأهيل المهني' ,'والاجتماعي للأشخاص',' ذوي الإعاقة' ,'مجموعة' ,'شيكلوتوف','لقد كنت ابحث عن وظيفة منذ ما يقرب من عام ','برفقة قهوة جيدة حصلت على وظيفة في شركة توصيل ','يتلقى الخدمة من مقهى جيد', 'في مجموعة جيدة ','لم أكن لأتمكن من النهوض من السرير ','اليوم لا اضيع مناوبة ! انه انجاز كبير جدا بالنسبة لي ','يتلقى الخدمة من مقهى جيد', 'في مجموعة جيدة' ,'بعد شهر ونصف من مرافقتي المهنية أصبحت منتجاً بقناةكان!!','يتلقى الخدمة منGOODJOB ','في مجموعة شيكلوتوف','بحث'])
@app.route('/FAQ' , methods= ('POST', "get"))
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
        msg = Message('Answer for question about out charity "shekulutov"', sender="shekulutov@outlook.com", recipients= ['jihadmagic@gmail.com'])
        msg.body = request.form['answer']
        mail.send(msg)
        try:
            x= request.form["popular"]
            question_and_answer=db.child('questions').child(UID).get().val()
            question_and_answer['answer']= request.form['answer']
            db.child('popular').push(question_and_answer )
        except:
            pass
        db.child('questions').child(login_session['UID']).remove()
    else:
        try:
            print (login_session['user'])
        except:
            return redirect(url_for('adminlogin'))
    try:
        UID = random.choice(list(db.child('questions').get().val()))
        login_session['UID']= UID    
        value=db.child('questions').get().val()[UID]
        login_session['recipientemail']= value['email']
        return render_template('admin.html', question=value)
    except: 
        return "all questions answered"

@app.route("/signout")
def signout():
    auth.current_user=None
    login_session['user']=None
    return (redirect(url_for('about')))

@app.route('/home_ar')
def home_arabic():
    return redirect(url_for("home", language="ar"))

@app.route('/', methods=['POST','GET'])
def home_hebrew():
    return redirect(url_for("home", language="he"))

@app.route('/home/<string:language>' ,methods=['POST', 'GET'])
def home(language):
    language = language.lower()
    return render_template('home.html', text= db.child('langueges').child(language).get().val(), language=language)
if __name__ == '__main__':
    app.run(debug=True)