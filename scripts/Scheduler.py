from apscheduler.schedulers.blocking import BlockingScheduler
from scripts.CourseStatus import *

courses = []
courses.append(CourseStatus('201908', '83870', False))
sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=3)
def timed_job():
    print(courses)

sched.start()