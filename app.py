from flask import render_template, redirect, request, Flask
from pathlib import Path
import shutil
import sqlite3
app = Flask(__name__, static_folder="assets")

files = []



def write_to_static(ogpath,localpath):
    src = Path(ogpath)
    result = Path(localpath)
    result.parent.mkdir(parents= True, exist_ok= True)
    if not src.is_dir():
        shutil.copy2(src,result)
    shutil.copytree(src,result,dirs_exist_ok=True)
    return "Resolved path successfully"

    


@app.route('/', methods=['GET', 'POST'])
def index():
    path = request.form.get("Path")
    
    report = None
    if path:
        p = Path(path)
        report = write_to_static(path,Path("static") / p.name)
    return render_template("index.html", prompt = report)

@app.route('/about',methods=['GET', 'POST'])
def about():
    return render_template("about.html")

@app.route('/repo',methods=['GET', 'POST'])
def repo():
    path = request.form.get("Path")
    
    
    return render_template("Repo.html")

if __name__ == '__main__':
    app.run(debug=True)

