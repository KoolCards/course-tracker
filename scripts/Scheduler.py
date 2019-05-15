from apscheduler.schedulers.blocking import BlockingScheduler
from CourseStatus import *
from Backend import *
import pyrebase
import os

config = {
    "apiKey": os.environ['CT_FIREBASE_KEY'],
    "authDomain": "course-tracker-11.firebaseapp.com",
    "databaseURL": "https://course-tracker-11.firebaseio.com",
    "storageBucket": "course-tracker-11.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

courses = {}
sched = BlockingScheduler()
backend = Backend()
coursecrns = []

@sched.scheduled_job('interval', seconds=3)
def trackCourses():
    course, status = backend.trackCourse(courses)
    print(courses)
    if (course is not None and status is not None):
        print('new update')
        if (status):
            backend.sendMessage(f'Course with crn: {course.crn} is open')
        else:
            backend.sendMessage(f'Course with crn: {course.crn} has closed')
    else:
        print('no updates')

@sched.scheduled_job('interval', seconds = 10)
def updateCourses():
    courseRawData = db.child('courses').get()
    removeCourses = courses.copy()
    print(removeCourses)
    if (courseRawData):
        try:
            for course in courseRawData.each():
                crn = course.key()
                term = course.val()
                if (crn not in coursecrns):
                    courses[CourseStatus(term, crn)] = backend.checkCourseStatus(term, crn)
                    coursecrns.append(crn)
                    print('began tracking')
                    backend.sendMessage(f'You began tracking course with crn: {crn} ')
                else:
                    removeCourses.pop(CourseStatus(term, crn))
        except TypeError:
            print('empty db')
    print(removeCourses)
    for key in removeCourses:
        courses.pop(key)

sched.start()