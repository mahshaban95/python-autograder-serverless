from distutils.log import debug
from email.policy import default
from importlib.resources import contents
import os
from unicodedata import name
from flask import Flask, render_template, flash, request, redirect, url_for
import pytest
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pathlib


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'py'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///score_board'
app.config['SERVER_NAME'] = '0.0.0.0'
db = SQLAlchemy(app)


class board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Submission %>' % self.id

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def lambda_handler(event, context):
    # if request.method == 'POST':

    #     try:
    #         board_name = request.form['name']
    #         new_record = board(name=board_name)

    #         try:
    #             db.session.add(new_record)
    #             db.session.commit()
    #             return redirect('/')
    #         except:
    #             print("DB add issue")

    #     except:
    #         print("Not a record submission")    

    #     # check if the post request has the file part
    #     if 'file' not in request.files:
    #         flash('No file part')
    #         return redirect(request.url)
    #     file = request.files['file']
    #     # If the user does not select a file, the browser submits an
    #     # empty file without a filename.
    #     if file.filename == '':
    #         flash('No selected file')
    #         return redirect(request.url)
    #     file.save("./uploads/assignment.py")
    #     #result = int(os.popen('python3 ./uploads/assignment.py 1 2').read())
    #     try:
    #         #retcode = pytest.main()
    #         #retcode = pytest.main(['--cache-clear', '-d --tx popen//python=python3.8',  'uploads/test_assignment1.py'])
    #         result = os.popen('py.test --cache-clear uploads/test_assignment1.py').read()
    #     except:
    #         render_template('wrong.html') 
    #     if result.find('passed') == -1:
    #         return render_template('wrong.html')
    #     else:
    #         return render_template('correct.html')
    retcode = pytest.main(['--cache-clear', 'uploads/test_assignment1.py'])
    print(retcode)
    with app.app_context():
        records = board.query.order_by(board.date_created).all()
        page = render_template('index.html', records=records)
        return {
            'statusCode': 200,
            'body': page,
            'headers': {
                'Content-Type': 'text/html',
            }
    }

