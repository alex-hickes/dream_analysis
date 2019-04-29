from Fralysis.SpacySetup import *
from Fralysis.Constants import *
from collections import defaultdict
import spacy
from spacy.tokens import Token
from spacy.tokens import Doc

class Subject(Enum):
    CLIENT = 1
    SOMEONE = 2
    OTHER = 3

#Class Dream contains all essential features of a dream. These include:
#Subjects : List[Token] - The essential tokens of a given dream. Defined by either containing a Topic/Description or Rating.
#Topics : Set(Topic) - The various Freudian topics found in the Dream.
#Rating : Rating - Overall rating of the Dream. This considers all Tokens with Rating attributes and combines for overall Rating.
class Dream:

    def __init__(self, message : Doc = None):

        self.messages = [message]

        self.subject = None

        self.direct_object = ""
        #TODO: Maybe make this work? should be a dictionary with three keys: Topic, Rating, Description. Rating may be none, but each entry shoudl contain a Topic and Description.
        self.tokens = defaultdict()

        self.topics = []

        self.rating = []

        self.descriptions = []

    def get_messages(self):
        return self.messages

    def get_latest_message(self):
        return self.messages[len(self.messages) - 1]

    def add_message(self, msg: Doc):
        self.messages.append(msg)

    def get_subject(self):
        return self.subject

    def set_subject(self, subject):
        self.subject = subject

    def get_direct_object(self):
        return self.direct_object

    def set_direct_object(self, direct_object):
        self.direct_object = direct_object

    def add_token(self, token):
        self.tokens.append(token)

    def get_tokens(self):
        return self.tokens

    def get_topics(self):
        return self.topics

    def add_topic(self, topic: Topic):
        self.topics.append(topic)

    def get_ratings(self):
        return self.rating

    def add_rating(self, rating: Rating):
        self.rating.append(rating)

    def get_descriptions(self):
        return self.descriptions

    def add_description(self, desc: str):
        self.descriptions.append(desc)

    def remove_duplicates(self):
        self.topics = list(dict.fromkeys(self.topics))
        self.descriptions = list(dict.fromkeys(self.descriptions))
