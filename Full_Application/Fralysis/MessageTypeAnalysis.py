from Fralysis.SpacySetup import *
from Fralysis.test.test_data import *
from Fralysis.Constants import *
from enum import Enum
from Fralysis.AnalyseDream import is_essential
from Fralysis.DreamValidator import Request

class MessageTypeAnalysis:
    """
    Class to identify whether a users input contains a name, dream or something irrelevant
    """

    def __init__(self, message: str = ""):

        """
        Initialises variables for MessageTypeAnalysis

        :type message: string
        :param message: user's input

        :type name: string
        :param name: user's name

        :type nlp: Language
        :param nlp: SpaCy NLP pipeline

        :type message_nlp: Doc
        :param message_nlp: user's input with attributes attached to tokens. This enables identification of Freudian features
        """

        self.message = message
        self.name = ""
        self.nlp = SpacySetup().get_nlp()
        self.message_nlp = None

    def is_miscellaneous(self):

        """
        Check if user greets chatbot or says something unrelated to dream analysis

        :return bool:
        """

        if self.message in GREETING_TERMS:
            return Miscellaneous.GREETING
        return False



    def is_name(self):

        """
        Check if user input contains their name
        """

        if self.name:
            return self.name

        message_nlp_titled = self.nlp(self.message.title())
        for sent in message_nlp_titled.sents:
            for token in sent:
                if (token.pos_ == "PROPN") or (token.text in VALID_NAME_LIST) and not (token.text in NOT_NAMES):

                    self.name = token.text
                    return self.name
        return False

    def is_option(self):

        """
        Check if user input contains a pre-analysis option
        """

        if self.message.lower() in MORE_INFO_RESPONSE:
            if DEBUG_ENABLED:
                print("3.1.3.1 - User has requested to provide more info - RETURN MORE_INFO")
            return PostOption.MORE_INFO
        elif self.message.lower() in NEW_DREAM_RESPONSE:
            if DEBUG_ENABLED:
                print("3.1.3.1 - User has requested to provide a new dream - RETURN NEW_DREAM")
            return PostOption.NEW_DREAM
        elif self.message.lower() in GET_ANALYSIS_RESPONSE:
            if DEBUG_ENABLED:
                print("3.1.3.1 - User has requested to get analysis - RETURN GET_ANALYSIS")
            return PostOption.GET_ANALYSIS
        else:
            if DEBUG_ENABLED:
                print("3.1.3.1 No option has been found - RETURN None")
            return None



    def is_dream(self, feature=None):

        """
        Check if user input contains features of a dream

        :param feature:
        :return SpaCy Doc: if user message contains dream features
        """

        if self.message_nlp is not None:
            if DEBUG_ENABLED:
                print("message_nlp is not None. message_nlp = {} - RETURN message_nlp".format(self.message_nlp))
            return self.message_nlp

        self.message_nlp = self.nlp(self.message)

        for sent in self.message_nlp.sents:

            if self.check_token(sentence=sent, feature=feature):

                if DEBUG_ENABLED:
                    print("Message contains features of a dream - RETURN nlp(message)")
                return self.message_nlp

        if DEBUG_ENABLED:
            print("Message doesn't contain features of a dream. Set message_nlp to None - RETURN None")
        self.message_nlp = None
        return None


    def check_token(self, sentence, feature=None):

        """
        Check if required tokens present

        :param sentence:
        :param feature:
        :return: list of valid tokens
        """

        valid_tokens = []
        for token in sentence:
            if is_essential(token) or token.text.strip(".").lower() in POS_SUBJECTS:
                valid_tokens.append(token)

        if feature is None:
            return valid_tokens
        if feature == Request.SUBJECT:
            return [token for token in valid_tokens if token.text.strip(".").lower() in POS_SUBJECTS]
        if feature == Request.TOPIC:
            return [token for token in valid_tokens if token._.topic is not None]
        if feature == Request.RATING:
            return [token for token in valid_tokens if token._.rating is not None]
