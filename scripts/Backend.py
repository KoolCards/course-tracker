from requests_html import HTMLSession
from twilio.rest import Client
import os

class Backend:
    def __init__(self):
        self.session = HTMLSession()
        self.account_sid = os.environ['TWILIO_SID']
        self.auth_token  = os.environ['TWILIO_TOKEN']
        pass

    def trackCourse(self, courses: dict) -> tuple:
        for course in courses:
            currSession = self.session.get(f'https://oscar.gatech.edu/pls/bprod/bwckschd.p_disp_detail_sched?term_in={course.term}&crn_in={course.crn}')
            remainingSeats = int(currSession.html.find('.dddefault')[3].text)
            waitlistSeats = int(currSession.html.find('.dddefault')[6].text)
            if (not courses[course] and (remainingSeats or waitlistSeats)):
                courses[course] = True
                return course, True
            elif(courses[course] and not (remainingSeats or waitlistSeats)):
                courses[course] = False
                return course, False
        return None, None

    def checkCourseStatus(self, term: str, crn: str):
        currSession = self.session.get(f'https://oscar.gatech.edu/pls/bprod/bwckschd.p_disp_detail_sched?term_in={term}&crn_in={crn}')
        remainingSeats = int(currSession.html.find('.dddefault')[3].text)
        waitlistSeats = int(currSession.html.find('.dddefault')[6].text)
        if (remainingSeats or waitlistSeats):
            return True
        return False

    def sendMessage(self, body: str):
        client = Client(self.account_sid, self.auth_token)
        message = client.messages.create(
            to="+14088059272",
            from_="+16153385525",
            body=body)
