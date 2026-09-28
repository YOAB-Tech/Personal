from flask import render_template, redirect, request, Flask, session, url_for, jsonify
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
import shutil
import sqlite3

from sqlalchemy import null, JSON

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
    file = db.Column(JSON,nullable=True)
    def __repr__(self):
        return f"User('{self.username}')"

@app.route('/')
def index():
    user = session.get('user')
    return render_template("index.html", prompt = user)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        result = db.session.execute(db.select(User).where(User.username == username)).scalar_one_or_none()
        if result:
            if password == result.password:
                session['user'] = result.username
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
        result = db.session.execute(db.select(User).where(User.username == username or User.email == email)).scalar_one_or_none()
        if result:
            if result.email == email:
                return render_template("register.html", prompt = "Email already exists")
            if result.username == username:
                return render_template("register.html", prompt = "Username already exists")
        id = db.session.execute(db.select(db.func.count()).select_from(User)).scalar()+1
        user = User(id = id, username = username, password = password, email = email, phonenumber = phonenumber, file = None)
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html")

@app.route('/homepage/<string:username>', methods=['GET', 'POST'])
def homepage(username):
    if 'user' not in session or session.get('user') is None:
        return redirect("/login")
    user = db.session.execute(db.select(User).where(User.username == username)).scalar_one_or_none()
    file_existence = user.file
    return render_template("homepage.html", file_existence = file_existence)

@app.route('/about',methods=['GET', 'POST'])
def about():
    return render_template("about.html")


@app.route('/repo',methods=['GET', 'POST'])
def repo():
    path = request.form.get("Path")
    return render_template("Repo.html")

@app.route('/upload/<string:username>',methods=['GET', 'POST'])
def upload(username):
    if request.method == 'POST':
        Path(f'Repo/{username}').mkdir(parents=True, exist_ok= True)
        personalfolder = Path(f'Repo/{username}')
        path = request.files.getlist("file")
        fileinfo = []
        for file in path:
            if not file.filename:
                continue
            relativepath = file.filename
            safe_path = Path(relativepath).as_posix()
            if '..'in safe_path or safe_path.startswith('/'):
                continue
            dest = personalfolder / relativepath
            dest.parent.mkdir(parents=True, exist_ok= True)
            file.save(dest)
            file.seek(0,2)
            filesize = file.tell()
            file.seek(0)
            fileinfo.append({
                "filename" : file.filename,
                "filepath": safe_path,
                "filesize" : filesize
            })
        user = db.session.execute(db.select(User).where(User.username == username)).scalar_one_or_none()

        db.session.commit()
    return render_template("upload.html")

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect("/")
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

