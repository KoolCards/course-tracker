from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
import time
from scripts.Backend import *
from scripts.CourseStatus import *
import os

app = Flask(__name__, static_folder='build/static', template_folder='build/')
CORS(app)
backend = Backend()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/submit", methods=['POST'])
def submit():
    crn = request.form['crn']
    term = request.form['term']
    course = CourseStatus(term, crn, False)
    file = open('courses.txt', 'a')
    file.write(course.crn + ' ' + course.term + '\n')
    file.close()
    return jsonify('This course has been added to the list to track')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 4000), debug=True)

