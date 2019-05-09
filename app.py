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
courses = []

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
        print(course.crn, status)
    print('no updates')

if __name__ == "__main__":
    courses.append(CourseStatus('201908', '83870', False))
    scheduler = BackgroundScheduler()
    scheduler.add_job(checkCourses, 'interval', seconds=3)
    scheduler.start()
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 4000), debug=True)

    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

