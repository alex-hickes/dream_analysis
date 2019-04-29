from enum import Enum
from Fralysis.Dream import Dream

#Enum for requests.
class Request(Enum):
    NAME = 1
    SUBJECT = 2
    DIR_OBJ = 3
    TOPIC = 4
    RATING = 5

class DreamValidator:

    def __init__(self, dream: Dream):
        self.dream_to_validate = dream

    def is_valid(self):
        if not self.outstanding_features():
            return True
        return False


    def outstanding_features(self):
        outstanding = []
        if not self.has_subject():
            outstanding.append(Request.SUBJECT)
        if not self.has_topic():
            outstanding.append(Request.TOPIC)
        if not self.has_rating():
            outstanding.append(Request.RATING)
        return outstanding


    def has_subject(self):
        if self.dream_to_validate.get_subject() is not None:
            return True
        return False

    def has_topic(self):
        if self.dream_to_validate.get_topics():
            return True
        return False

    def has_rating(self):
        if self.dream_to_validate.get_ratings():
            return True
        return False
