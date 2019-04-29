from Fralysis.SpacySetup import *
from Fralysis.test.test_data import *
from Fralysis.Constants import *
from enum import Enum

class MessageTypeAnalysis:

    def __init__(self, message: str = ""):
        self.message = message
        self.name = ""
        self.nlp = SpacySetup().get_nlp()
        self.message_nlp = None

    def is_name(self):

        if self.name:
            return self.name

        message_nlp_titled = self.nlp(self.message.title())
        for sent in message_nlp_titled.sents:
            for token in sent:
                if (token.pos_ == "PROPN") and not (token.text in NOT_NAMES):

                    self.name = token.text
                    return self.name
        return False

    #TODO: Don't think this is used anymore. Deleted or provide default response.
    #      May throw errors due to message_nlp, in which case instanciiate nlp in this method.
    def is_greeting(self):

        for sent in self.message_nlp.sents:
            for token in sent:
                if token.pos_ == "INTJ":
                    return True
        return False

    def is_miscellaneous(self):

        if self.message in GREETING_TERMS:
            return Miscellaneous.GREETING
        if self.message in WEATHER_TERMS:
            return Miscellaneous.WEATHER
        return False

    def is_option(self):

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



    def is_dream(self):

        if self.message_nlp is not None:
            if DEBUG_ENABLED:
                print("message_nlp is not None. message_nlp = {} - RETURN message_nlp".format(self.message_nlp))
            return self.message_nlp

        self.message_nlp = self.nlp(self.message)

        for sent in self.message_nlp.sents:
            for token in sent:
                if (token._.topic is not None) or (token._.rating is not None) or (token.text.strip(".").lower() in POS_SUBJECTS):
                    if DEBUG_ENABLED:
                        print("Message contains features of a dream - RETURN nlp(message)")
                    return self.message_nlp

        if DEBUG_ENABLED:
            print("Message doesn't contain features of a dream. Set message_nlp to None - RETURN None")
        self.message_nlp = None
        return False
