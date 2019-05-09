from requests_html import HTMLSession
from scripts.CourseStatus import *

class Backend:
    def __init__(self):
        self.session = HTMLSession()
        pass

    def trackCourse(self, courses: list) -> tuple:
        for course in courses:
            currSession = self.session.get(f'https://oscar.gatech.edu/pls/bprod/bwckschd.p_disp_detail_sched?term_in={course.term}&crn_in={course.crn}')
            remainingSeats = int(currSession.html.find('.dddefault')[3].text)
            waitlistSeats = int(currSession.html.find('.dddefault')[6].text)
            if (not course.isopen and (remainingSeats or waitlistSeats)):
                course.isopen = True
                return course, True
            elif(course.isopen and not (remainingSeats or waitlistSeats)):
                course.isopen = False
                return course, False
        return None, None