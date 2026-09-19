from flask import render_template, redirect, request, Flask,session,url_for
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
import shutil
import sqlite3
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///User.sqlite3'
app.config['SECRET_KEY'] = 'mysterious_yoab_admin_SECRET_KEY_cookie'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=True)
    phonenumber = db.Column(db.String(80), unique=True, nullable=True)
    filepath = db.Column(db.String(80), unique=True, nullable=True)
    def __repr__(self):
        return f"User('{self.username}')"
def write_to_static(ogpath,localpath):
    src = Path(ogpath)
    result = Path(localpath)
    result.parent.mkdir(parents= True, exist_ok= True)
    if not src.is_dir():
        shutil.copy2(src,result)
    shutil.copytree(src,result,dirs_exist_ok=True)
    return "Resolved path successfully"

    
id = 0

@app.route('/')
def index():
    user = session['username']
    return render_template("index.html", prompt = user)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        result = db.session.execute(db.select(User).where(User.username == username)).scalar_one_or_none()
        if result:
            if password == result.password:
                session['username'] = result.username
                return redirect(f"/homepage/{result.username}")
            else:
                return render_template("login.html",prompt = "Password does not match")
        else:
            return redirect("/register")
    return render_template("login.html")

@app.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        phonenumber = request.form.get("phoneNumber")
        result = db.session.execute(db.select(User).where(username == username)).scalar_one_or_none()
        if result:
            return render_template("register.html", prompt = "Username already exists")
        id = id +1
        user = User(id = id, username = username, password = password, email = email, phonenumber = phonenumber, filepath = None)
        db.session.add(user)
        db.session.commit()
        return render_template("login.html")
    return render_template("register.html")

@app.route('/homepage/<string:username>', methods=['GET', 'POST'])
def homepage(username):
    if 'username' not in session or session.get('username') is None:
        return redirect("/login")
    if request.method == 'POST':
        path = request.form.get("Path")
        p = Path(path)
        report = write_to_static(path,Path("Repo") / p.name )
        return render_template("homepage.html", prompt=report)
    return render_template("homepage.html")

@app.route('/about',methods=['GET', 'POST'])
def about():
    return render_template("about.html")


@app.route('/repo',methods=['GET', 'POST'])
def repo():
    path = request.form.get("Path")
    
    
    return render_template("Repo.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

