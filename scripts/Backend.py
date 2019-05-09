from requests_html import HTMLSession
from scripts.CourseStatus import *
from twilio.rest import Client

class Backend:
    def __init__(self):
        self.session = HTMLSession()
        self.account_sid = "AC0d31c18d6d286c0a6c0fc4dd12f61674"
        self.auth_token  = "673a74ff6d57f2a7e5c32f860960edde"
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

    def sendMessage(self, body: str):
        client = Client(self.account_sid, self.auth_token)
        message = client.messages.create(
            to="+14088059272",
            from_="+16153385525",
            body=body)
