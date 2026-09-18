from flask import render_template, redirect, request, Flask
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
import shutil
import sqlite3
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///User.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=True)
    phonenumber = db.Column(db.String(80), unique=True, nullable=True)
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

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        result = db.session.execute(db.select(User).where(User.username == username)).scalar_one_or_none()
        if result:
            if password == result.password:
                return redirect("/homepage")
        else:
            return redirect("/register")
    return render_template("index.html")

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
        user = User(id = id, username = username, password = password, email = email, phonenumber = phonenumber)
        db.session.add(user)
        db.session.commit()
    return render_template("register.html")

@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    report = None
    if request.method == 'POST':
        path = request.form.get("path")
        p = Path(path)
        report = write_to_static(path,Path("static") / p.name )

    return render_template("homepage.html", prompt = report)

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

