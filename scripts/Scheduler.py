from apscheduler.schedulers.blocking import BlockingScheduler
from CourseStatus import *
from Backend import *

courses = []
sched = BlockingScheduler()
backend = Backend()

@sched.scheduled_job('interval', seconds=3)
def trackCourses():
    course, status = backend.trackCourse(courses)
    print(courses)
    if (course is not None and status is not None):
        print('ayyoo')
        backend.sendMessage(f'Course with crn: {course.crn} has changed')
    print('no updates')

@sched.scheduled_job('interval', seconds = 10)
def updateCourses():
    courses.clear()
    file = open('../courses.txt', 'r')
    for line in file:
        crn, term = line.split(' ')
        courses.append(CourseStatus(term[:-1], crn, False))

sched.start()