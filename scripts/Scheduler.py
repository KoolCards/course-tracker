from apscheduler.schedulers.blocking import BlockingScheduler
from CourseStatus import *
from Backend import *
import pyrebase

config = {
    "apiKey": "AIzaSyAQNWWueglSwwcU9X07k5x-tlVC9wykCC4",
    "authDomain": "course-tracker-11.firebaseapp.com",
    "databaseURL": "https://course-tracker-11.firebaseio.com",
    "storageBucket": "course-tracker-11.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

courses = []
sched = BlockingScheduler()
backend = Backend()
coursecrns = []

@sched.scheduled_job('interval', seconds=3)
def trackCourses():
    course, status = backend.trackCourse(courses)
    print(courses)
    if (course is not None and status is not None):
        print('new update')
        backend.sendMessage(f'Course with crn: {course.crn} has changed')
    else:
        print('no updates')

@sched.scheduled_job('interval', seconds = 10)
def updateCourses():
    courseRawData = db.child('courses').get()
    if (courseRawData):
        try:
            for course in courseRawData.each():
                crn = course.key()
                term = course.val()
                if (crn not in coursecrns):
                    courses.append(CourseStatus(term, crn, False))
                    coursecrns.append(crn)
        except TypeError:
            print('empty db')

sched.start()