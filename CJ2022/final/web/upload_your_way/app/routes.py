# coding=utf-8

from flask import render_template, url_for, request
from app import app
import os
import string
import hashlib

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def random_dir():
    rand_str = hashlib.md5(os.urandom(16)).hexdigest()
    return rand_str

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == "GET":
        return render_template('upload.html')
    elif request.method == "POST":
        if 'file' not in request.files:
            return "no file"
        
        file_ = request.files['file']

        if file_.filename == '':
            return "no selected file"
        
        if file_ and allowed_file(file_.filename):
            filename = file_.filename

            if file_.content_length > 1 * 2048:
                return "max limit size"

            if not all(c.isalnum() or c in ".-" for c in filename):
                return "invalid filename"
            
            if ".." in filename:
                return "no traversal"

            folder = random_dir()
            os.mkdir("app/static/uploads/{}".format(folder))
            file_.save(os.path.join(os.path.join(os.getcwd(), "app/static/uploads/{}".format(folder)), filename))
            
            return render_template('upload.html', folder=folder)
        else:
            return "error"
        




