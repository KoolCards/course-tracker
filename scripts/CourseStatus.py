class CourseStatus:
    def __init__(self, term: str, crn: str):
        self.term = term
        self.crn = crn

    def __hash__(self):
        return hash((self.term, self.crn))

    def __eq__(self, other):
        return (self.term, self.crn) == (other.term, other.crn)