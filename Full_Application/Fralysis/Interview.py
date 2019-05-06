from Fralysis.Client import Client
from Fralysis.Conversation import Conversation
from Fralysis.InputOutput import InputOutput
from Fralysis.Constants import *

from Fralysis.AnalyseDream import match_dreams
from Fralysis.DreamValidator import DreamValidator


class Interview:
    """
    Class to Represents therapist's thought process and required proceedure to get to next checkpoint
    """

    def __init__(self, client: Client, in_out: InputOutput):

        """
        Initialise an interview between therapist and client

        :type client: Client
        :param client: The patient in question

        :type conversation: Conversation
        :param conversation: The actual means of chatting to user
        """

        self.client = client
        self.conversation = Conversation(in_out)

    def ask_for_name(self):

        """
        Retrieves name from user
        """

        if DEBUG_ENABLED:
            print("1.1 - Get a name as result from getting name -> Conversation")
        name = self.conversation.get_name()

        if name:
            if DEBUG_ENABLED:
                print("1.1 - Name is valid. Set clients name to name - RETURN client's name")
            self.client.set_name(name)
            return self.client.get_name()
        else:

            if DEBUG_ENABLED:
                print("1.2 - Name is empty - RETURN None")
            return None
    #TODO: Not fully sure whats happening here. We want to get a dream, remove duplicates and give to client.
    def ask_for_dream(self):

        """
        Retrieves complete dream from user
        """

        if DEBUG_ENABLED:
            print("2.1 - Get a dream as result from getting dream -> Conversation")
            print("TODO: IF NEW DREAM HAS BEEN CALLED, CONVERSATION'S DREAM SHOULD BE NONE")
        complete_dream = self.conversation.get_dream()

        if complete_dream is not None:
            if DEBUG_ENABLED:
                print("2.2 - Dream is valid. Remove duplicates *TODO: Duplicates no longer removed here* and set clients dram to dream - RETURN dream")
            #complete_dream.remove_duplicates()
            self.client.add_dream(complete_dream)
            return self.client.get_dream()
        else:

            if DEBUG_ENABLED:
                print("2.2 - dream is None - RETURN None")
            return None

    #TODO: After dream is complete, give user some options on what to do next:
    #      Provide another dream, give more details, or provide analysis.
    def provide_options(self):

        """
        Retrieves pre-analysis option from user
        """

        if DEBUG_ENABLED:
            print("3.1 - Request options from client -> Conversation")
        post_dream = self.conversation.get_post_analysis_option()

        if post_dream == PostOption.GET_ANALYSIS:
            if DEBUG_ENABLED:
                print("3.3 - User opted to get dream analysed - RETURN True")
            return True

        if post_dream == PostOption.NEW_DREAM:
            if DEBUG_ENABLED:
                print("3.3 - User opted to give another dream. go to - 2.1")
                print("TODO: CHECK IF BELOW WORKS!!!")
            self.conversation.dream = None

            if self.ask_for_dream() is not None:
                if DEBUG_ENABLED:
                    print("3.4 - Another dream has been collected and added successfully - RETURN True")
                return True
            else:
                if DEBUG_ENABLED:
                    print("3.4 - New dream was not successful - RETURN False")
                return False

        if DEBUG_ENABLED:
            print("TODO: This shouldn't be seen - RETURN False")
        return False

    def give_analysis(self):

        """
        Gives feedback to user about their dreams
        """

        if DEBUG_ENABLED:
            print("4.1 - For each dream a client has, give them an analysis. No of Dreams = {} -> conversation".format(len(self.client.get_dreams())))
        for dream in self.client.get_dreams():
            self.conversation.get_analysis(dream)


        if DEBUG_ENABLED:
            print("4.2 - Check if user has multiple dreams. No of dreams = {}".format(len(self.client.get_dreams())))
        if len(self.client.get_dreams()) > 1:
            if DEBUG_ENABLED:
                print("TODO: May have issues because of update to rating_matches in AnalyseDream ")
            matched_topics, matched_rating = match_dreams(self.client.get_dreams())
            if DEBUG_ENABLED:
                print("4.3 - User has multiple dreams. Compare all dreams. matched_topics = {}. matched_ratings = {} -> analyseDream".format(matched_topics, matched_rating))
                print("4.4 - Use comparison to provide combined_analysis -> conversation")
                print("    - RETURN matched topics and ratings")
            return self.conversation.get_combined_analysis(matched_topics, matched_rating)
