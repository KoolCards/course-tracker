from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
import time
from scripts.Backend import *
from scripts.CourseStatus import *
from scripts.Scheduler import *
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
    if (not course in courses):
        courses.append(course)
        return 'The course has been added'
    return 'The course is already being tracked'

def checkCourses():
    course, status = backend.trackCourse(courses)
    if (course is not None and status is not None):
        backend.sendMessage(f'Course with crn: {course.crn} has changed')
    print('no updates')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 4000), debug=True)

