from Fralysis.SpacySetup import *
from Fralysis.Constants import *
from collections import defaultdict
import spacy
from spacy.tokens import Token
from spacy.tokens import Doc

class Subject(Enum):

    """
    Enum for possible subjects of a dream
    """

    CLIENT = 1
    SOMEONE = 2
    OTHER = 3

#Class Dream contains all essential features of a dream. These include:
#Subjects : List[Token] - The essential tokens of a given dream. Defined by either containing a Topic/Description or Rating.
#Topics : Set(Topic) - The various Freudian topics found in the Dream.
#Rating : Rating - Overall rating of the Dream. This considers all Tokens with Rating attributes and combines for overall Rating.
class Dream:

    """
    Class to represent and hold information on a users dream
    """

    def __init__(self, message : Doc = None):

        """
        Initialised with a message from the user

        :param message:
        """

        self.messages = [message]

        self.subject = None

        self.direct_object = ""
        #TODO: Maybe make this work? should be a dictionary with three keys: Topic, Rating, Description. Rating may be none, but each entry shoudl contain a Topic and Description.
        self.tokens = defaultdict()

        self.topics = []

        self.rating = []

        self.descriptions = []

    def get_messages(self):

        """
        Get list of messages used to describe dream

        :return: list of messages
        """

        return self.messages

    def get_latest_message(self):

        """
        Get the latest message provided from the user about this dream
        :return: SpaCy Doc
        """

        return self.messages[len(self.messages) - 1]

    def add_message(self, msg: Doc):

        """
        Add message to describe dream

        :param msg:
        """

        self.messages.append(msg)

    def get_subject(self):

        """
        Get subject of dream

        :return: dream's subject
        """

        return self.subject

    def set_subject(self, subject):

        """
        Set the subject of a dream

        :param Subject:
        """

        self.subject = subject

    def get_direct_object(self):

        """
        Get the direct object of the dream

        :return: dream's direct object
        """

        return self.direct_object

    def set_direct_object(self, direct_object):
        """
        Set the direct object of a dream

        :param direct object string:
        """

        self.direct_object = direct_object

    def get_topic(self):

        """
        Get the latest symbol provided from the user about this dream
        :return Topic: Dream symbolism
        """

        return self.topics[len(self.topics) - 1]


    def get_topics(self):
        """
        Get the symbolism of a dream

        :return list of symbols:
        """

        return self.topics

    def add_topic(self, topic: Topic):
        """
        Add symbolisms of a dream

        :param Topic:
        """

        self.topics.append(topic)

    def get_ratings(self):
        """
        Get the sentiment of a dream

        :return sentiment:
        """

        return self.rating

    def add_rating(self, rating: Rating):
        """
        Add the sentiment of a dream

        :param Rating:
        """

        self.rating.append(rating)

    def get_descriptions(self):
        """
        Get the description of a dream

        :return description:
        """

        return self.descriptions

    def add_description(self, desc: str):
        """
        Describe the dream

        :param description string:
        """

        self.descriptions.append(desc)

    def remove_duplicates(self):
        """
        Remove duplicates in the dream
        """

        self.topics = list(dict.fromkeys(self.topics))
        self.descriptions = list(dict.fromkeys(self.descriptions))
